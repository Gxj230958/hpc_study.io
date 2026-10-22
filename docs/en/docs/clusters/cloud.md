# An Already Allocated Cloud GPU Instance

**Prerequisites:** An existing allocation, AWS CLI credentials with appropriate access, known region/instance ID and an approved budget. **Objective:** Inspect, use and clean up an allocated instance without provisioning.

These are optional examples, not commands executed by course validation. Provisioning, security-group changes, IAM changes and new storage are outside scope. Replace placeholders only for an instance assigned to you.

## Inspect the Allocation

```bash
aws sts get-caller-identity
aws ec2 describe-instances --region YOUR_REGION --instance-ids YOUR_INSTANCE_ID --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,State:State.Name,IP:PublicIpAddress}' --output table
```

Verify account, instance type, state and intended owner before using the allocation. Obtain the authorized SSH method from the allocation owner; after connecting, run the same local setup and bounded labs. A cloud instance label does not prove GPU visibility or driver readiness. See [AWS describe-instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html).

## Cost Worksheet

Use a dated quoted instance rate R, billed hours H, storage cost S and transfer cost D: estimated total = R*H+S+D. A hypothetical 4 currency-units/hour for three hours plus 2 storage and 1 transfer costs 15 units. This is arithmetic, not a current AWS price quote. Include setup, failed runs, idle time and retained storage in H/S.

## Cleanup an Allocation You May Stop

Copy evidence out first and confirm no other user's job depends on the instance. For an EBS-backed instance whose owner authorizes stopping:

```bash
aws ec2 stop-instances --region YOUR_REGION --instance-ids YOUR_INSTANCE_ID
aws ec2 wait instance-stopped --region YOUR_REGION --instance-ids YOUR_INSTANCE_ID
aws ec2 describe-instances --region YOUR_REGION --instance-ids YOUR_INSTANCE_ID --query 'Reservations[].Instances[].State.Name' --output text
```

These examples do not terminate an instance or delete data. Stopping can lose instance-store data, and retained volumes/public IP resources may continue incurring charges. Follow the allocation owner's resource cleanup process and verify billing state. See [stop-instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/stop-instances.html) and [EC2 lifecycle billing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html).

Next, return to [the distributed preflight](distributed.md). No AWS command is part of local or CI validation.
