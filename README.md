# aws_cleanup
Small python scripts to cleanup unused aws resources

## Direction
1. Configure your awscli environment in `~/.aws/credentials`
1. Modify `listXXX.py` and change `cutoff_date`
1. run `listXXX.py > output.csv` to generate a csv output of particular resource you're trying to remove
1. verify the csv list to make sure all resources are ok to delete
1. run `deleteXXX.py output.csv` to delete the particular resource from the list generated
