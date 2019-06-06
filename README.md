# Cloudformation-Dynamodb-Export

This command can parse Cloudformation templates, collect DynamoDB table properties and export them as JSON.

## Install

```
pip install cloudformation-dynamodb-export
```

## Usage

from the command line, you can run the command as below

```
cloudformation-dynamodb-export <template-file>
```

### Options

You can pass `Parameters` with `--param` option, so that we can solve `Fn::Sub` and `Fn::Ref` instrinsic functions.

```
cloudformation-dynamodb-export <template-file> --param StageName=prod --param AwsRegion=us-west-2
```

## License

MIT
