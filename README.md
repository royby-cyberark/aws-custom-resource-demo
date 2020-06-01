# aws-custom-resource-demo
CDK Demo implementing an S3 Object custom resource using AWSCustomResource  

* Clone this repo
* Activate virtual env: 
   * Linux/Macos: `source .env/bin/activate`
   * Windows: `.env\bin\activate`
* Install packages: `pip install -r requirements.txt`
* Optionally update the id in the CdkStack instantiation in app.py to set your stack name
* Deploy: `cdk deploy`

NOTE: Make sure that you have a working aws profile which you can deploy to.
if you're not sure, follow the "CDK Getting started guide"
