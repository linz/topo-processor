import { App } from "aws-cdk-lib";
import { AwsBatchStack } from "./batch";

const app = new App();
new AwsBatchStack(app, "Batch", {
  env: {
    region: "ap-southeast-2",
    account: process.env["CDK_DEFAULT_ACCOUNT"],
  },
  container: ".",
});
