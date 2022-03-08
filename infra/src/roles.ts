import { AwsAccountNames, AwsAccounts, AwsEnv } from '@linz/accounts';
import { CfnOutput, Stack } from 'aws-cdk-lib';
import { AccountPrincipal, Role } from 'aws-cdk-lib/aws-iam';
import { Bucket } from 'aws-cdk-lib/aws-s3';

export function createRolesForBucket(stack: Stack, bucket: Bucket): void {
  let geostorePrincipal = null;
  if (stack.account === AwsAccounts.byNameEnv(AwsAccountNames.Linz.Topography, AwsEnv.NonProduction).id) {
    const geostoreAccount = AwsAccounts.byNameEnv(AwsAccountNames.Linz.LiGeoStore, AwsEnv.NonProduction);
    geostorePrincipal = new AccountPrincipal(geostoreAccount.id);
    const geostoreRole = new Role(stack, 'Geostore', {
      roleName: 'geostore-s3-access-read',
      assumedBy: geostorePrincipal,
    });
    bucket.grantRead(geostoreRole);
    new CfnOutput(stack, 'GeostoreRoleReadArn', { value: geostoreRole.roleArn });
  } else if (stack.account === AwsAccounts.byNameEnv(AwsAccountNames.Linz.Topography, AwsEnv.Production).id) {
    const geostoreAccount = AwsAccounts.byNameEnv(AwsAccountNames.Linz.LiGeoStore, AwsEnv.Production);
    geostorePrincipal = new AccountPrincipal(geostoreAccount.id);
    const geostoreRole = new Role(stack, 'Geostore', {
      roleName: 'geostore-s3-access-read',
      assumedBy: geostorePrincipal,
    });
    bucket.grantRead(geostoreRole);
    new CfnOutput(stack, 'GeostoreRoleReadArn', { value: geostoreRole.roleArn });
  }
}
