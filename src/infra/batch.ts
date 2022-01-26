import { CfnOutput, Stack, StackProps } from "aws-cdk-lib";
import { DockerImageAsset } from "aws-cdk-lib/aws-ecr-assets";
import { ContainerImage } from "aws-cdk-lib/aws-ecs";
import {
  Role,
  CompositePrincipal,
  ServicePrincipal,
  CfnInstanceProfile,
  ManagedPolicy,
  PolicyStatement,
} from "aws-cdk-lib/aws-iam";
import {
  Vpc,
  InstanceClass,
  InstanceType,
  InstanceSize,
} from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";
import {
  ComputeResourceType,
  ComputeEnvironment,
  JobDefinition,
  JobQueue,
} from "@aws-cdk/aws-batch-alpha";

interface BatchStackProps extends StackProps {
  container: string;
}

export class AwsBatchStack extends Stack {
  public constructor(scope: Construct, id: string, props: BatchStackProps) {
    super(scope, id, props);

    const container = new DockerImageAsset(this, "BatchContainer", {
      directory: props.container,
    });
    const image = ContainerImage.fromDockerImageAsset(container);

    const vpc = Vpc.fromLookup(this, "AlbVpc", {
      tags: { BaseVPC: "true" },
    });
    const instanceRole = new Role(this, "BatchInstanceRole", {
      assumedBy: new CompositePrincipal(
        new ServicePrincipal("ec2.amazonaws.com"),
        new ServicePrincipal("ecs.amazonaws.com")
      ),
    });
    instanceRole.addManagedPolicy(
      ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AmazonEC2ContainerServiceforEC2Role"
      )
    );
    instanceRole.addManagedPolicy(
      ManagedPolicy.fromAwsManagedPolicyName("AmazonSSMManagedInstanceCore")
    );

    instanceRole.addToPrincipalPolicy(
      new PolicyStatement({ resources: ["*"], actions: ["sts:AssumeRole"] })
    );
    new CfnInstanceProfile(this, "BatchInstanceProfile", {
      instanceProfileName: instanceRole.roleName,
      roles: [instanceRole.roleName],
    });

    const computeEnvironment = new ComputeEnvironment(this, "BatchCompute", {
      managed: true,
      computeResources: {
        instanceRole: instanceRole.roleName,
        vpc,
        type: ComputeResourceType.SPOT,
        maxvCpus: 100,
        minvCpus: 0,
        desiredvCpus: 1,
        instanceTypes: [InstanceType.of(InstanceClass.C6G, InstanceSize.LARGE)],
      },
    });

    const job = new JobDefinition(this, "BatchJob", {
      container: { image },
    });
    const queue = new JobQueue(this, "BatchQueue", {
      computeEnvironments: [{ computeEnvironment, order: 1 }],
    });

    new CfnOutput(this, "BatchJobArn", { value: job.jobDefinitionArn });
    new CfnOutput(this, "BatchQueueArn", { value: queue.jobQueueArn });
  }
}
