from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = "#358140"

    stage_sql_template = """
    COPY {}
    FROM '{}'
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    REGION '{}'
    IGNOREHEADER 1
    CSV 
    """

    @apply_defaults
    def __init__(
        self,
        # Define your operators params (with defaults) here
        redshift_conn_id="redshift",
        aws_credentials_id="s3_connection",
        table="",
        s3_bucket="s3a://jsleslie-data-engineering-capstone-1.0",
        s3_key="",
        region="us-west-2",
        *args,
        **kwargs
    ):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region

    def execute(self, context):
        aws_hook = AwsBaseHook(self.aws_credentials_id, client_type = 's3')
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Copying data from S5 to Redshift")
        #         rendered_key = self.s3_key.format(**context)
        s3_loc = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        formatted_sql = self.stage_sql_template.format(
            self.table,
            s3_loc,
            credentials.access_key,
            credentials.secret_key,
            self.region
        )
        redshift.run(formatted_sql)
