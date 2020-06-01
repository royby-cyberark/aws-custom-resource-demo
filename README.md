# AWS Custom Resource Demo
CDK Demo implementing an S3 Object custom resource using AWSCustomResource  

**WARNING!** Deploying this projet will create some AWS resources. make sure you are aware of the costs and be sure to destory the stack when you are done by running `cdk destory`

**NOTE**: Make sure that you have a working aws profile which you can deploy to.

if you're not sure, follow the [CDK Getting started guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)

---

### Prerequisites:
* Working python environment with pip and venv

### Deploying the stack
* Clone this repo, change into the cdk dir
* Activate virtual env: 
   * Linux/Macos: `source .env/bin/activate`
   * Windows: `.env\bin\activate`
* Install packages: `pip install -r requirements.txt`
* Optionally update the id in the CdkStack instantiation in app.py to set your stack name
* Deploy: `cdk deploy`
* Do epic stuff

### Testing the custom resource
* After a successful deployment, open the CloudFormation stack, resources, click on the bucket resource and open the new object, inspect its content.
* Make changes to the object_content dict in cdk_stack.py, redeploy, check the object content and versions.
* Destory the stack, destruction is successful only if your resources is also destroyed.

### Wraping up
* Destory the stack: `cdk detroy`




