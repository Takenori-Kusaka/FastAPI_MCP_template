import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { FastApiMcpStack } from '../lib/fastapi-mcp-stack';

test('FastAPI MCP Stack Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new FastApiMcpStack(app, 'MyTestStack');
  // THEN
  const template = Template.fromStack(stack);

  // Lambda関数が作成されていることを確認
  template.hasResourceProperties('AWS::Lambda::Function', {
    Runtime: 'python3.10',
    Handler: 'app.main.handler',
    MemorySize: 512,
    Timeout: 30,
  });

  // API Gatewayが作成されていることを確認
  template.hasResourceProperties('AWS::ApiGateway::RestApi', {
    Name: 'MyTestStack',
  });

  // ロググループが作成されていることを確認
  template.hasResourceProperties('AWS::Logs::LogGroup', {
    RetentionInDays: 7,
  });
});
