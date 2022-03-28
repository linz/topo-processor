import { App } from 'aws-cdk-lib';
import { AwsBatchStack } from './batch';
import { AwsBatchMonitor } from './batch-monitor';

const app = new App();
new AwsBatchStack(app, 'TopoProcessorBatch', {
  env: {
    region: 'ap-southeast-2',
    account: process.env['CDK_DEFAULT_ACCOUNT'],
  },
  container: './',
});
new AwsBatchMonitor(app, 'TopoProcessorBatchMon', {
  env: {
    region: 'ap-southeast-2',
    account: process.env['CDK_DEFAULT_ACCOUNT'],
  },
});
