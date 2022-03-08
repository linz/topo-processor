import { CfnOutput, Duration, RemovalPolicy, Stack, StackProps } from 'aws-cdk-lib';
import { DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets';
import { ContainerImage } from 'aws-cdk-lib/aws-ecs';
import {
  Role,
  CompositePrincipal,
  ServicePrincipal,
  CfnInstanceProfile,
  ManagedPolicy,
  PolicyStatement,
} from 'aws-cdk-lib/aws-iam';
import { Vpc, InstanceClass, InstanceType, InstanceSize } from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';
import { ComputeResourceType, ComputeEnvironment, JobDefinition, JobQueue } from '@aws-cdk/aws-batch-alpha';
import { BlockPublicAccess, Bucket } from 'aws-cdk-lib/aws-s3';
import { StringParameter } from 'aws-cdk-lib/aws-ssm';
import { createRolesForBucket } from './roles';

interface BatchStackProps extends StackProps {
  container: string;
}

export class AwsBatchStack extends Stack {
  public constructor(scope: Construct, id: string, props: BatchStackProps) {
    super(scope, id, props);

    const container = new DockerImageAsset(this, 'BatchContainer', { directory: props.container });
    const image = ContainerImage.fromDockerImageAsset(container);

    const vpc = Vpc.fromLookup(this, 'Vpc', { tags: { BaseVPC: 'true' } });
    const instanceRole = new Role(this, 'BatchInstanceRole', {
      assumedBy: new CompositePrincipal(
        new ServicePrincipal('ec2.amazonaws.com'),
        new ServicePrincipal('ecs.amazonaws.com'),
      ),
    });
    instanceRole.addManagedPolicy(
      ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
    );
    instanceRole.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'));

    instanceRole.addToPrincipalPolicy(
      new PolicyStatement({ resources: ['*'], actions: ['sts:AssumeRole', 'cloudformation:DescribeStacks'] }),
    );

    const tempBucket = new Bucket(this, 'TempBucket', {
      removalPolicy: RemovalPolicy.RETAIN,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: [{ expiration: Duration.days(30) }],
    });
    createRolesForBucket(this, tempBucket);
    tempBucket.grantReadWrite(instanceRole);
    StringParameter.fromStringParameterName(this, 'BucketConfig', 'BucketConfig').grantRead(instanceRole);

    new CfnInstanceProfile(this, 'BatchInstanceProfile', {
      instanceProfileName: instanceRole.roleName,
      roles: [instanceRole.roleName],
    });

    const computeEnvironment = new ComputeEnvironment(this, 'BatchCompute', {
      managed: true,
      computeResources: {
        instanceRole: instanceRole.roleName,
        vpc,
        type: ComputeResourceType.SPOT,
        maxvCpus: 100,
        minvCpus: 0,
        instanceTypes: [
          InstanceType.of(InstanceClass.C5, InstanceSize.LARGE),
          InstanceType.of(InstanceClass.C5, InstanceSize.XLARGE),
          InstanceType.of(InstanceClass.C5, InstanceSize.XLARGE2),
          InstanceType.of(InstanceClass.C5, InstanceSize.XLARGE4),
        ],
      },
    });

    const job = new JobDefinition(this, 'BatchJob', { container: { image } });
    const queue = new JobQueue(this, 'BatchQueue', { computeEnvironments: [{ computeEnvironment, order: 1 }] });

    new CfnOutput(this, 'BatchJobArn', { value: job.jobDefinitionArn });
    new CfnOutput(this, 'BatchQueueArn', { value: queue.jobQueueArn });
    new CfnOutput(this, 'BatchEc2InstanceRole', { value: instanceRole.roleArn });
    new CfnOutput(this, 'TempBucketName', { value: tempBucket.bucketName });
  }
}
