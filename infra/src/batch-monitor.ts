import { Stack, StackProps } from 'aws-cdk-lib';
import * as events from 'aws-cdk-lib/aws-events';
import * as evtTargets from 'aws-cdk-lib/aws-events-targets';
import * as lf from 'aws-cdk-lib/aws-lambda';
import { Code } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as path from 'path';

export class AwsBatchMonitor extends Stack {
  public constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    const rule = new events.Rule(this, 'BatchEventRule', {
      eventPattern: {
        source: ['aws.batch'],
        detailType: ['Batch Job State Change'],
      },
    });

    const lambda = new lf.Function(this, 'BatchLog', {
      runtime: lf.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: Code.fromAsset(path.join(process.cwd(), 'infra', 'src', 'lambda-code')),
    });

    rule.addTarget(new evtTargets.LambdaFunction(lambda));
  }
}
