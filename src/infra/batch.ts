import cdk = require('@aws-cdk/core');
import batch = require('@aws-cdk/aws-batch');
import ec2 = require('@aws-cdk/aws-ec2');
import ecrAssets = require('@aws-cdk/aws-ecr-assets');
import ecs = require('@aws-cdk/aws-ecs');
import * as iam from '@aws-cdk/aws-iam';
import { CfnOutput } from '@aws-cdk/core';

interface BatchStackProps extends cdk.StackProps {
  container: string;
}

export class AwsBatchStack extends cdk.Stack {
  public constructor(scope: cdk.Construct, id: string, props: BatchStackProps) {
    super(scope, id, props);

    const container = new ecrAssets.DockerImageAsset(this, 'BatchContainer', {
      directory: props.container,
    });
    const image = ecs.AssetImage.fromDockerImageAsset(container);

    const vpc = ec2.Vpc.fromLookup(this, 'AlbVpc', { tags: { BaseVPC: 'true' } });
    const instanceRole = new iam.Role(this, 'BatchInstanceRole', {
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal('ec2.amazonaws.com'),
        new iam.ServicePrincipal('ecs.amazonaws.com'),
      ),
    });
    instanceRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
    );
    instanceRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'));

    instanceRole.addToPrincipalPolicy(new iam.PolicyStatement({ resources: ['*'], actions: ['sts:AssumeRole'] }));
    new iam.CfnInstanceProfile(this, 'BatchInstanceProfile', {
      instanceProfileName: instanceRole.roleName,
      roles: [instanceRole.roleName],
    });

    const computeEnvironment = new batch.ComputeEnvironment(this, 'BatchCompute', {
      managed: true,
      computeResources: {
        instanceRole: instanceRole.roleName,
        vpc,
        type: batch.ComputeResourceType.SPOT,
        maxvCpus: 100,
        minvCpus: 0,
        desiredvCpus: 1,
        instanceTypes: [ec2.InstanceType.of(ec2.InstanceClass.C5, ec2.InstanceSize.LARGE)],
      },
    });

    const job = new batch.JobDefinition(this, 'BatchJob', { container: { image } });
    const queue = new batch.JobQueue(this, 'BatchQueue', { computeEnvironments: [{ computeEnvironment, order: 1 }] });

    new CfnOutput(this, 'BatchJobArn', { value: job.jobDefinitionArn });
    new CfnOutput(this, 'BatchQueueArn', { value: queue.jobQueueArn });
  }
}
