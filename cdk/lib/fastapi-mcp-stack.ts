import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class FastApiMcpStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda関数のログ設定
    const logGroup = new logs.LogGroup(this, 'FastApiMcpLogs', {
      logGroupName: `/aws/lambda/fastapi-mcp-${this.node.tryGetContext('stage') || 'dev'}`,
      retention: logs.RetentionDays.ONE_WEEK,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Lambda関数の作成
    const handler = new lambda.Function(this, 'FastApiMcpFunction', {
      runtime: lambda.Runtime.PYTHON_3_10,
      code: lambda.Code.fromAsset('../', {
        bundling: {
          image: lambda.Runtime.PYTHON_3_10.bundlingImage,
          command: [
            'bash', '-c', [
              'pip install -r requirements/prod.txt -t /asset-output',
              'cp -r app /asset-output/',
              'cp -r scripts /asset-output/',
            ].join(' && '),
          ],
        },
      }),
      handler: 'app.main.handler',
      memorySize: 512,
      timeout: cdk.Duration.seconds(30),
      environment: {
        PYTHONPATH: '/var/task',
        STAGE: this.node.tryGetContext('stage') || 'dev',
      },
      logGroup,
    });

    // API Gatewayの作成
    const api = new apigateway.LambdaRestApi(this, 'FastApiMcpApi', {
      handler,
      proxy: true,
      deployOptions: {
        stageName: this.node.tryGetContext('stage') || 'dev',
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    // 出力
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
      description: 'FastAPI MCP API URL',
    });
  }
}
