![AWS_IoT_Core.png](img/AWS_IoT_Core.png)

<a id="Top"></a>
## AWS IoT Device Management Workshop
This workshop will guide you through the features of [AWS IoT Device Management](https://aws.amazon.com/iot-device-management/).

The workshop is designed to be conducted on an EC2 instance which will be provisioned through AWS CloudFormation. Amazon Linux is used as operating system and the standard user is named *ec2-user*. 

We do provide some scripts that you will use in the workshop. They are copied automatically into the directory *~/bin* of the user *ec2-user* on your EC2 instance. 

You will also create a Lambda function during the workshop and the code can be found in *~/lambda*.

For several exercises the aws command line interface (awscli) is used. It is installed and configured automatically on the EC2 Instance.

## Workshop Agenda

* [Prerequisites](#Prerequisites)
* [Launch an EC2 Instance with CloudFormation](#Launch_EC2_Instance_with_CloudFormation)
* [Enable Logging for AWS IoT](#Enable_Logging_IoT)
* [Registry Events](#Registry_Events)
* [Device Provisioning with the API](#Device_Provisioning_with_the_API)
* [Single Device Provisioning](#Single_Device_Provisioning)
* [Bulk Device Provisioning](#Bulk_Device_Provisioning)
* [JITP - Just-in-Time Provisioning](#JITP)
* [JITR - Just-in-Time Registration](#JITR)
* [IoT Jobs](#IoT_Jobs)
* [Fleet Indexing](#Fleet_Indexing)
* [Thing Groups](#Thing_Groups)
* [Fine-Grained Logging](#Fine-Grained_Logging)
* [Clean Up](#Cleanup)

<a id="Prerequisites"></a>
[[Top](#Top)]
## Prerequisites
To conduct the workshop you will need the following tools/setup/knowledge:

* AWS Account
* Secure shell (ssh) to login into the EC2 instance
	* Mac OS/Linux: command lines tools are installed by default
	* Windows
		* Putty: ssh client: <http://www.putty.org/>
		* Manual connect (ssh) to an EC2 instance from Windows with Putty: <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html>
* A ssh key-pair to be able to log into the EC2 instance
	* a ssh key-pair can be generated or imported in the AWS console under *EC2 -> Key Pairs*
* Basic knowledge how to move around on a linux system and edit files

### Recommendation
Don't use a production account to conduct this workshop to not mess up things accidentally. Use an AWS region where you do not have provisioned any IoT resources to avoid conflicts during creating or deleting resources.


<a id="Launch_EC2_Instance_with_CloudFormation"></a>
[[Top](#Top)]
## Launch an EC2 Instance with AWS CloudFormation

For the exercises in this workshop an EC2 instance will be used. We do provide a [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) stack to create an EC2 instance and other AWS resources required for this workshop. Simply click the AWS region where you want to launch your stack. It is recommended to choose the closest region.

By choosing one of the links below you will be automatically redirected to the CloudFormation section of the AWS Console where your stack will be launched.

#### Prior to launch the CloudFormation stack you need to have:

* **An ssh key pair to log into the EC2 instance. If you don't have an ssh key pair you can create one in the** 
	
	=> *EC2 console -> Key pairs*

The CloudFormation Stack creates the following resources:

* **S3 Bucket** required for Bulk Provisioning
* **IoT Policy** for provisioning scenarios
* **VPC with public subnet + Security Group** for an EC2 instance
* **EC2 instance** where you do your work
* **Instance Profile** for your EC2
* **IAM Role** required for provisioning scenarios

---

#### Prepare to launch the CloudFormation stack
To bootstrap the EC2 instance with the scripts for this workshop a tar file has to be pulled onto the instance during launch. The CloudFormation template is designed to get the tar file from a static S3 website.

##### Create an S3 bucket

**Go to the S3 console**

* \+ Create bucket
* Bucket name: **enter a bucket name** (will be referred to as CFN\_S3\_BUCKET)
* Next
* Next
* Next
* Create bucket
* Choose the bucket that you just have created
* Properties
* Static website hosting
* Use this bucket to host a website
* Index document: **index.html**
* Error document: **error.html**
* Take a note of your website URL. It has the format **http://\<bucket\>.s3-website.\<aws_region\>.amazonaws.com**
* Save 

##### Modify the CloudFormation template

* CloudFormation template: [**cfn/cfn-iot-dm-ws.json**](cfn/cfn-iot-dm-ws.json)
* Replace the string **YOUR\_STATIC\_S3\_WEBSITE** in the template with the URL of your static S3 website


##### Upload the tar file to S3

* Upload the file **dm-ws.tar** to the **CFN\_S3\_BUCKET**
* Make the file publicly readable. This can be done in the properties section of the file in the S3 console.

#### Launch the CloudFormation stack

Choose one of the following regions to launch the CloudFormation stack. The link will guide you directly to the AWS CloudFormation console

* [Launch CloudFormation stack in eu-central-1](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new) (Frankfurt)
* [Launch CloudFormation stack in eu-west-1](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new) (Ireland)
* [Launch CloudFormation stack in eu-west-2](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new) (London)
* [Launch CloudFormation stack in us-east-1](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new) (N. Virginia)
* [Launch CloudFormation stack in ap-south-1](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new) (Mumbai)
* [Launch CloudFormation stack in us-west-2](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new) (Oregon)
* [Launch CloudFormation stack in ap-southeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new) (Sydney)
* [Launch CloudFormation stack in ap-northeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new) (Tokyo)

After you have been redirected to the AWS CloudFormation console take the following steps to launch you stack:

1. Choose a template
2. Upload a template to Amazon S3
3. Select your modified CloudFormation template
4. Next
5. Stack name: **IoTDeviceManagementWS**
6. Parameters
7. Select SSHKeyName
8. Next
9. Next
10. Capabilities
11. Check "I acknowledge that AWS CloudFormation might create IAM resources." at the bottom of the page
12. Create
13. If the stack does not appear immediately hit the refresh button in the upper right corner
14. Click on **IoTDeviceManagementWS**
15. Wait until the complete stack has been created 

Creating the stack should take round about 5mins.

If encounter any error(s) during stack creation look for the root cause in the Events section of the CloudFormation console. The most common error is to run into service limits.

In the **Outputs** section for your stack in the CloudFormation console you find several values for resources that has been created. These values will be used during the workshop:

* Name of an S3 bucket
* Name of an IoT policy
* ARN of a role that is used for device provisioning
* SSH login information
* ARN of a role required for a Lambda function

You can go back at any time to the Outputs section to get these values.

* ssh into your instance
	* you can find the hostname in the outputs section of the CloudFormation console

* You should find at least the directories/files in the home directory of the ec2-user:
	* bin
	* CA
	* job-agent
	* lambda
	* templateBody.json


<a id="Enable_Logging_IoT"></a>
[[Top](#Top)]
## Enable Logging for AWS IoT

AWS IoT sends progress events about each message as it passes from your devices through the message broker and the rules engine. To view these logs, you must configure AWS IoT to generate the logs used by CloudWatch.

To enable [AWS IoT logging](https://docs.aws.amazon.com/iot/latest/developerguide/cloud-watch-logs.html), you must create an IAM role, register the role with AWS IoT, and then configure AWS IoT logging.

Go to the AWS IAM console

1. Roles
2. Create role
3. AWS service 
4. IoT
5. Next: Permissions
6. At least the following managed policy should already be chosen: AWSIoTLogging
7. Next: Review
4. Role name: AWSIoTAccessServices
5. Create Role

Go to the AWS IoT console

1. Get started (only if no resources are provisioned)
2. Settings
3. Logs (if DISABLED) -> Edit
4. Change "Level of verbosity" to "Warnings"
5. Set role -> Select "AWSIoTAccessServices"
6. Update


The log files from AWS IoT are send to **Amazon CloudWatch**. The AWS console can be used to look at these logs.


<a id="Registry_Events"></a>
[[Top](#Top)]
## Registry Events
The [Registry publishes event messages](https://docs.aws.amazon.com/iot/latest/developerguide/registry-events.html) when things, thing types, and thing groups are created, updated, or deleted.
Each event causes a single event message to be published by the service. Messages are published over MQTT with a JSON payload. The content of the payload depends on the type of event. 

The device registry posts messages to 

	$aws/events/# 
	
for several actions, e.g. when things are created/updated/deleted. 

**In this exercise** you will enable IoT Events. You will use IoT Events in the following exercises in this workshop.


#### Get event configuration
With the following command you can determine which IoT Events are enabled/disabled

	aws iot describe-event-configurations
	
#### Enable all events
Use the following command to enable all events:
	
	aws iot update-event-configurations --cli-input-json \
	'{
	    "eventConfigurations": {
	        "THING_TYPE": {
	            "Enabled": true
	        }, 
	        "JOB_EXECUTION": {
	            "Enabled": true
	        }, 
	        "THING_GROUP_HIERARCHY": {
	            "Enabled": true
	        }, 
	        "CERTIFICATE": {
	            "Enabled": true
	        }, 
	        "THING_TYPE_ASSOCIATION": {
	            "Enabled": true
	        }, 
	        "THING_GROUP_MEMBERSHIP": {
	            "Enabled": true
	        }, 
	        "CA_CERTIFICATE": {
	            "Enabled": true
	        }, 
	        "THING": {
	            "Enabled": true
	        }, 
	        "JOB": {
	            "Enabled": true
	        }, 
	        "POLICY": {
	            "Enabled": true
	        }, 
	        "THING_GROUP": {
	            "Enabled": true
	        }
	    }
	}'


<a id="Device_Provisioning_with_the_API"></a>
[[Top](#Top)]
## Device Provisioning with the API
**In this exercise** you will execute all the required commands to create and register a device with AWS IoT. Furthermore you will experience how registry events work.

A device that should be able to communicate with AWS IoT needs to have a X.509 certificate which is registered with AWS IoT as well as a IoT policy. X.509 certificates are used for authentication and the IoT policy for authorisation.

Several API calls are required to provision a device. The output for some commands is stored in files in /tmp because values from it are required for further steps in the provisioning chain.

In the previous section you have enable IoT Events. To see the messages that the device registry publishes subscribe to the related topic hierarchy. Use the builtin MQTT client in the AWS console to subscribe to topics.

* Go to the AWS IoT Console
	
	1. Test
	2. Subscribe to a topic
	3. Subscription topic: **$aws/events/#**
	4. Subscribe to topic

	
### Get root CA certificates

Server certificates allow your devices to verify that they're communicating with AWS IoT and not another server impersonating AWS IoT: <https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html>

A shell script is provided on the EC2 instance to download the CA certificates.

* ssh into your EC2 instance and run the following command:

		create-root-ca-bundle.sh
		
The CA certificates are stored as **$HOME/root.ca.bundle.pem**

### Create a Device

Use API calls to provision a device. A device is provisioned in AWS IoT when it has been created in the device registry, a device certificate has been registered and attached to the device, an IoT policy has been attached to the device.

* ssh into your EC2 instance:

		# putting your thing name into variable makes the next steps easier
		THING_NAME=my-first-thing
		
		# create a thing in the thing registry
		aws iot create-thing --thing-name $THING_NAME

* Go to the AWS IoT console:  
You should see a message that was posted to
	
		$aws/events/thing/$THING_NAME/created

* Go to your EC2 instance:
		
		# create key and certificate for your device and active the device
		aws iot create-keys-and-certificate --set-as-active \
		  --public-key-outfile $THING_NAME.public.key \
		  --private-key-outfile $THING_NAME.private.key \
		  --certificate-pem-outfile $THING_NAME.certificate.pem > /tmp/create_cert_and_keys_response
		
		# look at the output from the previous command
		cat /tmp/create_cert_and_keys_response
		
		# output values from the previous call needed in further steps
		CERTIFICATE_ARN=$(jq -r ".certificateArn" /tmp/create_cert_and_keys_response)
		CERTIFICATE_ID=$(jq -r ".certificateId" /tmp/create_cert_and_keys_response)
		echo $CERTIFICATE_ARN
		echo $CERTIFICATE_ID
		
		# create an IoT policy
		POLICY_NAME=${THING_NAME}_Policy
		aws iot create-policy --policy-name $POLICY_NAME \
		  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action": "iot:*","Resource":"*"}]}'
		
		# attach the policy to your certificate
		aws iot attach-policy --policy-name $POLICY_NAME \
		  --target $CERTIFICATE_ARN
		
		# attach the certificate to your thing
		aws iot attach-thing-principal --thing-name $THING_NAME \
		  --principal $CERTIFICATE_ARN
	
* List things in the device registry. Don't trust the AWS IoT console. It might not be aware of every update made through the API

		aws iot list-things
		
### Update the Device
To update the device you just created add an attribute. Also this modification of the device causes the device registry to publish an event message.

* Update the device

		aws iot update-thing --thing-name $THING_NAME --attribute-payload '{"attributes": {"type": "ws-device"}}'
		
* Look at your device

		aws iot list-things
	
* Go to the AWS IoT console:  
You should see a message that was posted to
	
		$aws/events/thing/$THING_NAME/updated
		
### Publish a message with you newly created device
After your device has been provisioned you will publish a message to AWS IoT. To publish a message the command *mosquitto_pub* is used. This command requires the iot endpoint to talk to.


* Subscribe to the topic **iot/ws**

* Go to your EC2 instance:

		# the iot endpoint has been already assigned to the shell variable $IOT_ENDPOINT but you can retrieve it with the following command:
		aws iot describe-endpoint
		
		# during setup of the EC2 instance the iot endpoint has already been assigned to the shell variable IOT_ENDPOINT

		# publish a message
		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		--cert $THING_NAME.certificate.pem \
		--key $THING_NAME.private.key -h $IOT_ENDPOINT -p 8883 \
		-q 0 -t iot/ws -i $THING_NAME --tls-version tlsv1.2 \
		-m "{\"prov\": \"first\", \"date\": \"$(date)\"}" -d
		
* Go to the AWS IoT Console and check if a message has arrived


<a id="Single_Device_Provisioning"></a>
[[Top](#Top)]
## Single Device Provisioning
**In this exercise** you will provision a single device with the [*register-thing*](https://docs.aws.amazon.com/iot/latest/developerguide/programmatic-provisioning.html) API call. In this provisioning example the thing will be assigned to a thing group and a thing type will be assigned. Group and type must exist before the provisioning is started.

Provision a thing with a single API call (register-thing) and a provisioning template. A key for the device and a CSR are also required to provision the device. 

You will find a provisioning template in your home directory. The filename is *templateBody.json*

Create keys, CSR and input parameter with the script *mk-prov.sh* for a single device. The output is applied through the Parameters section in the provisioning template to the register-thing API.

The device that will be created will also be put into a thing group and a thing type will be assigned. This is done through the provisioning template. However group and type must **exist before** the provisioning process starts.


* Create a thing group in AWS IoT

		aws iot create-thing-group --thing-group-name bulk-group

* Create a thing type in AWS IoT		
		
		aws iot create-thing-type --thing-type-name bulk-type

* Create key, CSR and parameters:

		# set you thing name
		THING_NAME=my-second-thing
		
		mk-prov.sh $THING_NAME

* Provision the thing. Copy the output between the curly brackets including the curly brackets and replace it in the following command in the --parameters section

		aws iot register-thing --template-body file://templateBody.json --parameters '[OUTPUT_FROM_THE_PREVIOUS_COMMAND]'
		
* As output from the previous command you receive the certificate for your thing. Copy the certificate pem from the output and save it into a file with the following command

		echo -e [CERTIFICATE_PEM] > $THING_NAME.crt
	
* Go to the AWS IoT Console:

		1. Manage
		2. Things
		3. Click on you thing
		4. Security
		5. Click the certificate
		6. Policies
		7. Click the Policy name

	
* Go to the AWS IoT Console:

		1. Subscribe to the topic: iot/ws

* Go to your EC2 instance:

		# publish a message to AWS IoT
		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		  --cert $THING_NAME.crt --key $THING_NAME.key \
		  -h $IOT_ENDPOINT -p 8883 -q 0 -t iot/ws \
		  -i $THING_NAME --tls-version tlsv1.2 \
		  -m "{\"prov\": \"second\", \"date\": \"$(date)\"}" -d
		
* Go to the AWS IoT Console and check if a message has arrived


<a id="Bulk_Device_Provisioning"></a>
[[Top](#Top)]
## Bulk Device Provisioning
**In this exercise** you will bulk provision multiple things with one API call: [*start-thing-registration-task*](https://docs.aws.amazon.com/iot/latest/developerguide/bulk-provisioning.html)

The API call **start-thing-registration-task** can be used to provision things in bulk. To provision things in bulk you need the same parameters as with single device provisioning with the **register-thing** API call. But you will put multiple parameters into file which then must be stored in an Amazon S3 bucket. 

An IAM role is also required to allow AWS IoT to access the S3 bucket and provision devices in your account. The role was created already through CloudFormation. You can find the required role ARN in the outputs section of the CloudFormation stack.

The parameters file which you need to store in the Amazon S3 bucket contains the values used to replace the parameters in the template. The file must be a newline-delimited JSON file. Each line contains all of the parameter values for provisioning a single device.

You can create keys, CSR and input parameter with the script *mk-bulk.sh* for multiple devices. The script mk-bulk.sh will create a directory and put all the keys, CSRs and a file **bulk.json** into this directory.  

To create a bulk provisioning the required S3 bucket must exist in the **same region** where the devices should be provisioned. This bucket was already created for the workshop and can be found in the shell variable **S3_BUCKET**

	
* Create keys and CSRs:

		THING_NAME=bulky
		
		# number of things to create
		NUM_THINGS=20
		
		mk-bulk.sh $THING_NAME $NUM_THINGS
		
		
* Keys, CSRs and the file **bulk.json** are created in a directory with the naming-scheme *$THING_NAME-YYYY-mm-dd_H-M-S*

* Copy the file *bulk.json* to your S3 bucket and verify that it was copied. The name of your S3 bucket has been copied during the setup of the workshop to the shell variable *S3_BUCKET*

		# cd to the directory where keys/CSRs where created
		cd $THING_NAME-YYYY-mm-dd_H-M-S
		
		# copy bulk.json to S3
		aws s3 cp bulk.json s3://$S3_BUCKET/
		
		# verify that the file was copied
		aws s3 ls s3://$S3_BUCKET/

* Create a bulk thing registration task. The name of your role has been copied during the setup of the workshop to the shell variable *$ARN\_IOT\_PROVISIONING\_ROLE*

		aws iot start-thing-registration-task \
		  --template-body file://~/templateBody.json \
		  --input-file-bucket $S3_BUCKET \
		  --input-file-key bulk.json --role-arn $ARN_IOT_PROVISIONING_ROLE

* If the command is successful you'll get back a task-id. You can verify the state of the task for ERRORS or RESULTS with the following commands:

		aws iot list-thing-registration-task-reports \
		  --report-type ERRORS --task-id [YOUR_TASK_ID] 

		aws iot list-thing-registration-task-reports \
		  --report-type RESULTS --task-id [YOUR_TASK_ID]		
		
* If you get output from the report-type RESULTS from the command above you can download the output for this command from a URL. The output will be stored in the file **results.json**

		wget -O results.json $(aws iot list-thing-registration-task-reports --task-id [YOUR_TASK_ID] --report-type RESULTS | jq -r '.resourceLinks[]')
		
* If you encounter errors use the following command to download the error messages. They are stored in the file **errors.json**. Examine the messages and solve the root cause.

		wget -O errors.json $(aws iot list-thing-registration-task-reports --task-id [YOUR_TASK_ID] --report-type ERRORS | jq -r '.resourceLinks[]')
		
* Take a look at the file **results.json**
* Write all the certificates from the file results.json to files for the related thing. Do it on your own or use a python script that we have prepared

		bulk-result.py results.json
	
* Verify that the certificates have been written

		ls -l
		
* List the things in the AWS IoT device registry

		aws iot list-things

* Now try to publish with one of the things that you created. Subscribe to the topic "iot/ws" before

		# replace XX with a number of the things you created
		THING_NAME=bulkyXX
		
		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		  --cert $THING_NAME.crt --key $THING_NAME.key \
		  -h $IOT_ENDPOINT -p 8883 -q 0 -t iot/ws \
		  -i $THING_NAME	 --tls-version tlsv1.2 \
		  -m "{\"prov\": \"bulk\", \"date\": \"$(date)\"}" -d
		
* **Exercise:** publish with all the things that you bulk provisioned
		

<a id="JITP"></a>
[[Top](#Top)]
## JITP - Just-in-Time Provisioning
You can have your devices provisioned when they first attempt to connect to AWS IoT. [Just-in-time provisioning](https://docs.aws.amazon.com/iot/latest/developerguide/jit-provisioning.html) (JITP) settings are made on CA certificates. You must enable automatic registration and associate a provisioning template with the CA certificate used to sign the device certificate you are using to provision the device. 

For JITP you need to bring your own CA. 

**In this exercise** you will create your own CA, register it with AWS IoT, prepare the CA for JITP and register a new device simply by connecting to AWS IoT.

* Change to the directory "CA"

		cd ~/CA

* Generate a key pair for your own CA

    	openssl genrsa -out rootCA.key 2048

* Use the private key from the key pair to generate a CA certificate

    	openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem
    	
* You will be prompted for some information. 
 
    	Country Name (2 letter code) [XX]:DE
		State or Province Name (full name) []:Berlin
		Locality Name (e.g., city) [Default City]:Berlin
		Organization Name (e.g., company) [Default Company Ltd]:IoT
		Organisational Unit Name (e.g., section) []:Workshop
		Common Name (e.g., your name or your server's hostname) []:IoT Workshop CA
		Email Address []:

* Register CA certificate
* Get a registration code from AWS IoT. This code will be used as the Common Name of the private key verification certificate

    	aws iot get-registration-code

* Generate a key pair for the private key verification certificate

    	openssl genrsa -out verificationCert.key 2048

* Create a CSR for the private key verification certificate. Set the **Common Name** to the registration code that you received above

    	openssl req -new -key verificationCert.key -out verificationCert.csr

* You will be prompted for some information. As common name set the registration code that you got from the "aws iot get-registration-code" command

		Country Name (2 letter code) [XX]: 
		State or Province Name (full name) []: 
		Locality Name (for example, city) []: 
		Organization Name (for example, company) []:
		Organisational Unit Name (for example, section) []:
		Common Name (e.g. server FQDN or YOUR name) []:XXXXXXXXXXXXYOURREGISTRATIONCODEXXXXXX 
		Email Address []:

* Create a certificate from the CSR

    	openssl x509 -req -in verificationCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out verificationCert.pem -days 500 -sha256

* Register the CA certificate with AWS IoT by using the certificate that you just created

    	aws iot register-ca-certificate --ca-certificate file://rootCA.pem --verification-cert file://verificationCert.pem
    	
* Verify that the CA certificate has been registered successfully. You received the ca certificate id in the output from the command above

		# assign the certificate id to a shell variable (for convenience)
		CA_CERTIFICATE_ID=[YOUR_CA_CERTIFICATE_ID]

		# verify registration
		aws iot describe-ca-certificate --certificate-id $CA_CERTIFICATE_ID

* Activate the CA certificate. The certificate-id was in the output of the previous command.

    	aws iot update-ca-certificate --new-status ACTIVE --certificate-id $CA_CERTIFICATE_ID

* Enable JITP for your CA by attaching a provisioning template to the CA. The required certificate id was already used in the previous command. The role arn required for JITP has been stored in the shell variable *$ARN\_IOT\_PROVISIONING\_ROLE*
		
		# store the template body in a shell 
		TB="{ \\\"Parameters\\\" : { \\\"AWS::IoT::Certificate::Id\\\" : { \\\"Type\\\" : \\\"String\\\" }, \\\"AWS::IoT::Certificate::CommonName\\\" : { \\\"Type\\\" : \\\"String\\\" }, \\\"AWS::IoT::Certificate::Country\\\" : { \\\"Type\\\" : \\\"String\\\" } }, \\\"Resources\\\" : { \\\"thing\\\" : { \\\"Type\\\" : \\\"AWS::IoT::Thing\\\", \\\"Properties\\\" : { \\\"ThingName\\\" : {\\\"Ref\\\" : \\\"AWS::IoT::Certificate::CommonName\\\"}, \\\"AttributePayload\\\" : { \\\"Country\\\" :  {\\\"Ref\\\" : \\\"AWS::IoT::Certificate::Country\\\"} }, \\\"ThingGroups\\\" : [\\\"bulk-group\\\"] } }, \\\"certificate\\\" : { \\\"Type\\\" : \\\"AWS::IoT::Certificate\\\", \\\"Properties\\\" : { \\\"CertificateId\\\": { \\\"Ref\\\": \\\"AWS::IoT::Certificate::Id\\\" }, \\\"Status\\\" : \\\"ACTIVE\\\" } }, \\\"policy\\\" : { \\\"Type\\\" : \\\"AWS::IoT::Policy\\\", \\\"Properties\\\" : { \\\"PolicyName\\\": \\\"$IOT_POLICY\\\" } } } }"
		
		# verify the content of $TB
		echo $TB
		
		# attach the provisioning template (stored in the variable $TB) to the CA certificate
		aws iot update-ca-certificate --certificate-id $CA_CERTIFICATE_ID \
  		  --no-remove-auto-registration \
  		  --new-auto-registration-status ENABLE \
  		  --registration-config "{\"templateBody\": \"$TB\",\"roleArn\": \"$ARN_IOT_PROVISIONING_ROLE\"}"
		
		
* Get information about your CA certificate and verify that the provisioning template has been attached

		aws iot describe-ca-certificate --certificate-id $CA_CERTIFICATE_ID

* Create a device certificate

	Name for your device cert
	
		deviceCert=deviceJITPCert
		
    Generate a key pair.

    	openssl genrsa -out $deviceCert.key 2048

    Create a CSR for the device certificate.

    	openssl req -new -key $deviceCert.key -out $deviceCert.csr

    You will be prompted for some information, as shown here.  
    **Fill in at least Country Name and Common Name as these values from the certificate are used to provision your device.**

	    Country Name (2 letter code) [XX]: 
	    State or Province Name (full name) []:
	    Locality Name (for example, city) []:
	    Organization Name (for example, company) []:
	    Organisational Unit Name (for example, section) []:
	    Common Name (e.g. server FQDN or YOUR name) []: my-jitp-device
	    Email Address []:
	    
	    Please enter the following 'extra' attributes
		to be sent with your certificate request
		A challenge password []:
		An optional company name []:

    Create a device certificate from the CSR.
    
		# issue certificate
    	openssl x509 -req -in $deviceCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out $deviceCert.pem -days 500 -sha256
    	
    	# put device cert and cert of your CA in one file
    	cat $deviceCert.pem rootCA.pem > ${deviceCert}AndCACert.crt

* In the AWS IoT console subscribe to **$aws/events/#**
* Auto register your device by publishing a message

    	# publish
    	mosquitto_pub --cafile ~/root.ca.bundle.pem \
    	  --cert ${deviceCert}AndCACert.crt --key $deviceCert.key \
    	  -h $IOT_ENDPOINT -p 8883 -q 1 -t  ji/tp \
    	  -i  $deviceCert --tls-version tlsv1.2 -m '{"let-me": "in"}' -d

* The command will produce an error message like:

		Client [device_name] sending CONNECT
		Error: The connection was lost.
	
* This is a **normal behaviour** as AWS IoT disconnects the client when the automatic registration of the device has been started.


* Verify if the device was created either in the AWS IoT Console or on the command line

		aws iot list-things
		
* Subscribe to **ji/tp** and publish again the message above. The device should be now provisioned and ready to operate

		# publish
    	mosquitto_pub --cafile ~/root.ca.bundle.pem \
    	  --cert ${deviceCert}AndCACert.crt --key $deviceCert.key \
    	  -h $IOT_ENDPOINT -p 8883 -q 1 -t  ji/tp -i $deviceCert \
    	  --tls-version tlsv1.2 -m '{"let-me": "in"}' -d

    
    
<a id="JITR"></a>
[[Top](#Top)]
## JITR - Just-in-Time Registration
When you connect to AWS IoT with the device certificate for the first time, the service will detect an unknown certificate signed by a registered CA and will auto-register the device certificate. On successful registration AWS IoT will publish a registration message on a reserved MQTT topic and disconnect the client. 

This MQTT registration event will trigger an AWS Lambda function through an [IoT topic rule](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html). The Lambda function will complete the provisioning of the device. After these steps, your device will be ready to work with AWS IoT.

**In this exercise** you will setup JITR with your own CA and an AWS Lambda function. When creating the device the lambda function will generate a thing name which starts with *jitr-* followed by the certificate id. The thing name will look similar to *jitr-12345435e8912702c16da3b3f8b91d085f7c0028d91ae7be53a1e7aa8160b3db*

* You should still have stored the certificate id in the shell variable *$CA_CERTIFICATE_ID*. **If not** store the certificate id into that variable

		CA_CERTIFICATE_ID=[YOUR_CA_CERTIFICATE_ID]
		
* First we need to remove JITP from the CA.  

		aws iot update-ca-certificate --certificate-id $CA_CERTIFICATE_ID \
		  --remove-auto-registration \
		  --new-auto-registration-status DISABLE

* Verify that the provision template an role arn have been removed from the CA

		aws iot describe-ca-certificate --certificate-id $CA_CERTIFICATE_ID
    
* Enable Just-in-Time Registration (JITR)

		aws iot update-ca-certificate --certificate-id $CA_CERTIFICATE_ID \
		  --new-auto-registration-status ENABLE
		
* Verify that the auto registration status is set to ENABLE

		aws iot describe-ca-certificate --certificate-id $CA_CERTIFICATE_ID
		
		
* Create a Lambda function. The role that is required to create the Lambda function was already created for you and copied to the shell variable *$ARN\_LAMBDA\_ROLE*

		# change to the directory where the lambda is stored
		cd ~/lambda

		# create the lambda function
		aws lambda create-function \
		--region $AWS_REGION \
		--function-name jitr \
		--zip-file fileb://lambda_function.zip \
		--role $ARN_LAMBDA_ROLE \
		--handler lambda_function.lambda_handler \
		--runtime python2.7 \
		--timeout 30 \
		--memory-size 128
		
		# verify that the lambda has been created
		aws lambda list-functions 

* Create an IoT topic rule. With this rule the Lambda function that you just created is called when a device certificate is auto-registered

		# to create the topic rule we need to have the arn of the Lambda function
		# Store the Lambda function arn in a shell variable
		ARN_LAMBDA=$(aws lambda get-function --function-name jitr | jq -r '.Configuration.FunctionArn')
		
		# verify the variable content
		echo $ARN_LAMBDA
		
		# create the IoT topic rule
		aws iot create-topic-rule --rule-name JITRRule \
		  --topic-rule-payload "{
            \"sql\": \"SELECT * FROM '\$aws/events/certificates/registered/#' WHERE certificateStatus = \\\"PENDING_ACTIVATION\\\"\",
            \"description\": \"Rule for JITR\",
            \"actions\": [
		            {
		                \"lambda\": {
		                    \"functionArn\": \"$ARN_LAMBDA\"
		                }
		            }
		        ]
		     }"
		  
* Verify that the topic rule has been created
		
		aws iot get-topic-rule --rule-name JITRRule
		
* Add a permission to the lambda to allow the AWS IoT to invoke the function. For adding the permissions we need the topic rule arn and will store it into a shell variable
				
		# get you AWS account id
		ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
		
		# verify that the variable has been set
		echo $ACCOUNT_ID

		# store topic rule arn
		ARN_TOPIC_RULE=$(aws iot get-topic-rule --rule-name JITRRule | jq -r '.ruleArn')
		
		# verify that the variable has been set
		echo $ARN_TOPIC_RULE

		# add permissions to the Lambda
		aws lambda add-permission --function-name jitr \
		  --region $AWS_REGION --principal iot.amazonaws.com \
		  --source-arn $ARN_TOPIC_RULE --source-account $ACCOUNT_ID \
		  --statement-id Id-123 --action "lambda:InvokeFunction"
		  
		# verify the permissions of the function
		aws lambda get-policy --function-name jitr


* Create device certificate in the same way you did for JITP but use a different name for the deviceCert

	Go to the certs directory
	
		cd ~/CA

	Name for your device cert
	
		deviceCert=deviceJITRCert

	Create a thing key, certificate and connect to AWS IoT like you did in the JITP section of this workshop.

	Connect to AWS IoT to initiate the JITR process  
	
		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		  --cert ${deviceCert}AndCACert.crt --key $deviceCert.key \
		  -h $IOT_ENDPOINT -p 8883 -q 1 -t  ji/tr -i $deviceCert \
		  --tls-version tlsv1.2 -m '{"let-me": "in"}' -d

	
* To verify if JITR was successful you should:
	* Have a look in the device registry (hint: aws iot list-things)
	* Look at the CloudWatch logs for the lambda and AWS IoT: **AWS CloudWatch Console -> Logs -> /aws/lambda/jitr**


<a id="IoT_Jobs"></a>
[[Top](#Top)]
## IoT Jobs
[AWS IoT Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) is a service that allows you to define a set of remote operations that are sent to and executed on one or more devices connected to AWS IoT. 

#### Job Topics
AWS IoT provides an MQTT API for jobs and uses the following topics:

* $aws/things/\<thingName\>/jobs/notify (or $aws/things/\<thingName\>/jobs/notify-next)
* $aws/things/\<thingName\>/jobs/get/accepted
* $aws/things/\<thingName\>/jobs/get/rejected
* $aws/things/\<thingName\>/jobs/jobId/get/accepted
* $aws/things/\<thingName\>/jobs/jobId/get/rejected

**In this exercise** you will create a job which will be gathered by a sample job agent. The job agent then acts based on the contents of the job document. The job agent uses the MQTT API to retrieve jobs and also to report the result of the executed job.  
You will find the job agent as *~/job-agent/job-agent.py*


* **Provision a device** with one of the options that you have learned in the **previous exercises** and put the root.ca.bundle.crt, device key and device cert into the directory *~/job-agent/*. E.g:

		cd ~/job-agent/
		THING_NAME=job-agent
		aws iot create-thing --thing-name $THING_NAME
		aws iot create-keys-and-certificate --set-as-active \
		  --public-key-outfile $THING_NAME.public.key \
		  --private-key-outfile $THING_NAME.private.key \
		  --certificate-pem-outfile $THING_NAME.certificate.pem > /tmp/create_cert_and_keys_response
		CERTIFICATE_ARN=$(jq -r ".certificateArn" /tmp/create_cert_and_keys_response)
		CERTIFICATE_ID=$(jq -r ".certificateId" /tmp/create_cert_and_keys_response)
		POLICY_NAME=${THING_NAME}_Policy
		aws iot create-policy --policy-name $POLICY_NAME \
		  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action": "iot:*","Resource":"*"}]}'
		aws iot attach-policy --policy-name $POLICY_NAME \
		  --target $CERTIFICATE_ARN
		aws iot attach-thing-principal --thing-name $THING_NAME \
		  --principal $CERTIFICATE_ARN

	
* List things in the device registry. Don't trust the AWS IoT console. It might not be aware of every update made through the API

		aws iot describe-thing --thing-name $THING_NAME


* **Start the sample job agent**. To start the job agent you need to provide on the command line the client-id, iot-endpoint, ca certificate, device key and certificate
		
		# when you have used the commands above to create the device
		./job-agent.py -c $THING_NAME -i $IOT_ENDPOINT \
		  --cacert ~/root.ca.bundle.pem --cert $THING_NAME.certificate.pem \
		  --key $THING_NAME.private.key

Go to the AWS IoT Console

1. Test
2. Subscribe to a topic
3. Subscription topic: **$aws/events/#**
4. Subscribe
5. Subscribe to a topic
6. Subscription topic: **$aws/things/#**
7. Subscribe
8. Subscribe to a topic
9. Subscription topic: **sys/info**
10. Subscribe


#### Sample job document
The following sample job document was already copied to your EC2 instance to *~/job-agent/job-document.json*

	{
	    "operation": "sys-info",
	    "sys-info": "uptime",
	    "topic": "sys/info"
	}
	
The intention of the job document is to instruct the job agent to get the uptime from the system that is running on and report it to AWS IoT Core to the topic *sys/info*

* ssh into the EC2 instance in an additional session. The job agent running in another session should not be interrupted.
* Copy the job document to your S3 Bucket

		cd ~/job-agent/
		# copy the document
		aws s3 cp job-document.json s3://$S3_BUCKET/
		
		# verify that the document has been copied
		aws s3 ls s3://$S3_BUCKET/
		
* Create a job. The job id that you choose must be unique. It is not possible to reuse a job id.
		
		# retrieve the arn for the job device, 
		# e.g. through list-things, describe-thing, "Manage" in the AWS IoT console
		JOB_THING_ARN=[ARN_OF_YOUR_JOB_THING]
		
		# define a unique job id
		JOB_ID=[an_id_e.g. 468]
		
		# finally create the job
		aws iot create-job --job-id  $JOB_ID \
			--targets $JOB_THING_ARN \
			--document-source https://s3.amazonaws.com/$S3_BUCKET/job-document.json  \
			--presigned-url-config "{\"roleArn\":\"$ARN_IOT_PROVISIONING_ROLE\", \"expiresInSec\":3600}" 
		
* You should receive an output similar to the following:
	
		{
		    "jobArn": "arn:aws:iot:[AWS_REGION]:[AWS_ACCOUNT_ID]:job/$JOB_ID", 
		    "jobId": "$JOB_ID"
		}

* Watch the output of the job-agent.py in the other session
* As long as there are no jobs present you should find a log line which contains:
	* **callback\_jobs\_get\_accepted - NO jobs available**
* After you have created your job you should see more activity in the logs. When a job is available you should find a log line containing:
	* **callback\_jobs\_get\_accepted - JOBS AVAILABLE** 
* Feel free to create more jobs


<a id="Fleet_Indexing"></a>
[[Top](#Top)]
## Fleet Indexing
[Fleet Indexing](https://docs.aws.amazon.com/iot/latest/developerguide/iot-indexing.html) is a managed service that allows you to index and search your registry and shadow data in the cloud. After your fleet index is set up, the service manages the indexing of all your registry and shadow updates. You can use a simple query language based on the popular open source search engine, Apache Lucene, to search across this data. 

**In this exercise** you will enable fleet indexing for the registry and the shadow and then perform searches in the registry. 

Let's assume you manage a building with a temperature sensor per room. You want to find out in which of the rooms the temperature is above 20° because that might be an indicator that the air condition is not working properly.

We will simulate temperature sensors by adding reported temperatures to the device shadows and adding also a room number attribute to devices. We will use the devices that you have created in the bulk provisioning exercise.

* Enable fleet indexing for the registry and shadow

		aws iot update-indexing-configuration \
		  --thing-indexing-configuration thingIndexingMode=REGISTRY_AND_SHADOW

* Verify if fleet indexing is enabled for both registry and shadow

		aws iot get-indexing-configuration

* Add reported temperature to the device shadow and room number to the device. We provide a small script that modifies all things matching the thing name *"name\*"*. Use the devices that you have created in the bulk provisioning exercise. We assume that you have used the thing name *bulky* in the earlier bulk provisioning exercise. If another name has been used, change the name in the following command accordingly. 

		# add temperature and room number 
		# to all devices matching the name "bulky*"
		# if you have named the devices in the bulk provisioning section
		# differently, choose the appropriate basename
		fleet-indexing.py -b bulky
		
	If you get an **error message** containing *Creation of index AWS_Things is in progress* it means that the indexing process has not finished yet. Wait some minutes and try again.
		
* Verify that the modification was successful. Every device from the bulk provisioning exercise should have an attribute *room\_number* and a reported temperature in the *shadow*

		aws iot search-index --query-string "thingName:bulky*"

* Find all device in the registry which have a room number and where the temperature is greater than 20°
		
		aws iot search-index \
		--query-string "shadow.reported.temperature>20 AND attributes.room_number:*"
		
* You can find the shadow document for a device also in the AWS IoT Console

	1. Go to the AWS IoT Console
	2. Manage
	3. Things
	4. Click on a thing
	5. Shadow
	6. Find the shadow state in the shadow document
	

<a id="Thing_Groups"></a>
[[Top](#Top)]
## Thing Groups
[Thing groups](https://docs.aws.amazon.com/iot/latest/developerguide/thing-groups.html) allow you to manage several things at once by categorizing them into groups. 

**In this exercise** you will learn how you can authorise devices by attaching an IoT policy to a thing group instead to a device certificate. The policy attached to the thing group will make use of policy variables so that a device is only allowed to publish to:   

	telemetry/building/one/${iot:ClientId}

Create a thing group policy, attach the policy to the thing group, create a device and add the device to the thing group.
 

* Go to your EC2 instance:

		# create a thing group
		THING_GROUP_NAME=building-one
		aws iot create-thing-group \
		  --thing-group-name $THING_GROUP_NAME > /tmp/create_group_response
		GROUP_ARN=$(jq -r ".thingGroupArn" /tmp/create_group_response)
		
		# get your AWS account id. It is required for the IoT policy in this example
		ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
		
		# create IoT policy
		POLICY_NAME=SmartBuilding_Policy
		aws iot create-policy --policy-name $POLICY_NAME \
		--policy-document "{\
	    \"Version\": \"2012-10-17\",\
	    \"Statement\": [{\
	        \"Effect\": \"Allow\",
	        \"Action\": [\"iot:Connect\"],\
	        \"Resource\": [\
	            \"arn:aws:iot:$AWS_REGION:$ACCOUNT_ID:client/\${iot:ClientId}\"\
	        ]\
	    },\
	    {\
	        \"Effect\": \"Allow\",\
	        \"Action\": [\"iot:Publish\"],\
	        \"Resource\": [\
	            \"arn:aws:iot:$AWS_REGION:$ACCOUNT_ID:topic/telemetry/building/one/\${iot:ClientId}\"\
	        ]\
	      }]\
	  	}"  	  	
	  	
		# attach policy to thing group
		aws iot attach-policy \
		  --target $GROUP_ARN \
		  --policy-name $POLICY_NAME
		  
		# verify that the policy was attached to the thing group
		aws iot list-attached-policies --target $GROUP_ARN

* Create a thing as well as key and certificate. Choose any method that you have learned earlier. **But DO NOT attach a policy to the device certificate**

		cd
		THING_NAME=group-member
		aws iot create-thing --thing-name $THING_NAME
		aws iot create-keys-and-certificate --set-as-active \
		  --public-key-outfile $THING_NAME.public.key \
		  --private-key-outfile $THING_NAME.private.key \
		  --certificate-pem-outfile $THING_NAME.certificate.pem > /tmp/create_cert_and_keys_response
		CERTIFICATE_ARN=$(jq -r ".certificateArn" /tmp/create_cert_and_keys_response)
		CERTIFICATE_ID=$(jq -r ".certificateId" /tmp/create_cert_and_keys_response)
		aws iot attach-thing-principal --thing-name $THING_NAME \
		  --principal $CERTIFICATE_ARN
		
* Add your thing to the thing group

		aws iot add-thing-to-thing-group \
		  --thing-name $THING_NAME \
		  --thing-group-name $THING_GROUP_NAME
		  
		# list things in your group
		aws iot list-things-in-thing-group \
		  --thing-group-name $THING_GROUP_NAME
		
* Subscribe in the AWS IoT console to **telemetry/building/one/#**
* Publish a message to the topic *telemetry/building/one/$THING_NAME*. You should see that the message is arriving.

		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		  --cert $THING_NAME.certificate.pem \
		  --key $THING_NAME.private.key -h $IOT_ENDPOINT -p 8883 \
		  -q 0 -t telemetry/building/one/$THING_NAME -i $THING_NAME --tls-version tlsv1.2 \
		  -m "{\"group\": \"test\", \"date\": \"$(date)\"}" -d
		
* Publish a message to another topic, this messages should not arrive.

		mosquitto_pub --cafile ~/root.ca.bundle.pem \
		  --cert $THING_NAME.certificate.pem \
		  --key $THING_NAME.private.key -h $IOT_ENDPOINT -p 8883 \
		  -q 0 -t telemetry/building/one/${THING_NAME}_foo -i $THING_NAME --tls-version tlsv1.2 \
		  -m "{\"group\": \"test\", \"date\": \"$(date)\"}" -d

<a id="Fine-Grained_Logging"></a>
[[Top](#Top)]
## Fine-Grained Logging
[Fine-grained logging](https://docs.aws.amazon.com/iot/latest/developerguide/cloud-watch-logs.html) allows you to specify a logging level for a target. A target is defined by a resource type and a resource name. Currently, AWS IoT supports thing groups as targets. Fine-grained logging allows you to set a logging level for a specific thing group. Fine-grained logs are stored in log group *AWSIotLogsV2*.

**In this exercise** you will learn how to set the log level for a thing group that is different from the global log level. The global log level has been set to WARN. For a particular thing group you will set a more verbose log level. Then you will create some log entries by publishing messages with the device you used in the previous section. Then you will use different filters to search the logs.

	
* Use the thing group *building-one* that you have created earlier
	
		THING_GROUP_NAME=building-one

* Get the current logging configuration
	
		aws iot get-v2-logging-options 

* Set the logging level to DEBUG for the thing group

		aws iot set-v2-logging-level --log-level DEBUG \
	  	  --log-target "{\"targetType\": \"THING_GROUP\", \"targetName\": \"$THING_GROUP_NAME\"}"
	  	  
	  	# verify the logging level
	  	aws iot list-v2-logging-levels

* Publish messages like you did in the previous section to a topic where you are allowed to publish and also to topics where you don't have permissions to publish
* Wait some minutes because it can take a small amount of time until logs are delivered to CloudWatch 
* Now let's search in the logs for events in the last hour

		# calculate the milliseconds since the epoch minus 1h
		starttime=$(($(($(date '+%s') - 3600)) * 1000))
	
		# search all logs in the last hour without any filters
		aws logs filter-log-events --log-group-name AWSIotLogsV2 \
		  --start-time $starttime 
	
		# search all logs where the log level is INFO
		aws logs filter-log-events --log-group-name AWSIotLogsV2 \
		  --start-time $starttime --filter-pattern "{$.logLevel = INFO}"
		  
		# search all logs where the log level is ERROR
		aws logs filter-log-events --log-group-name AWSIotLogsV2 \
		  --start-time $starttime --filter-pattern "{$.logLevel = ERROR}"
	
		# search for log entries from your thing used 
		aws logs filter-log-events --log-group-name AWSIotLogsV2 \
		  --start-time $starttime --filter-pattern "{$.clientId = $THING_NAME}"


<a id="Cleanup"></a>
[[Top](#Top)]
## Clean Up
With the following steps you can delete the resources created during the workshop.

### On your EC2 instance issue the following commands:

#### Disable all events
Use the following command to disable all events:
	
	aws iot update-event-configurations --cli-input-json \
	'{
	    "eventConfigurations": {
	        "THING_TYPE": {
	            "Enabled": false
	        }, 
	        "JOB_EXECUTION": {
	            "Enabled": false
	        }, 
	        "THING_GROUP_HIERARCHY": {
	            "Enabled": false
	        }, 
	        "CERTIFICATE": {
	            "Enabled": false
	        }, 
	        "THING_TYPE_ASSOCIATION": {
	            "Enabled": false
	        }, 
	        "THING_GROUP_MEMBERSHIP": {
	            "Enabled": false
	        }, 
	        "CA_CERTIFICATE": {
	            "Enabled": false
	        }, 
	        "THING": {
	            "Enabled": false
	        }, 
	        "JOB": {
	            "Enabled": false
	        }, 
	        "POLICY": {
	            "Enabled": false
	        }, 
	        "THING_GROUP": {
	            "Enabled": false
	        }
	    }
	}'

#### Delete the resources
Deleting the resources that where created during the workshop is a semi-automated process. We start with deprecating the thing type.

* First action is to deprecate the thing type as it will take round about 5 minutes to finish

		# deprecate the thing type
		aws iot deprecate-thing-type --thing-type-name bulk-type
		
		
* The things that you have created can be deleted by a script. **WARNING** this script uses the prefixes for devices in the workshop, *bulky* for the bulk provisioned devices and *jitr-* for device provisioned through JITR. 

**IF YOU HAVE ANY DEVICES CREATED OUTSIDE OF THIS WORKSHOP WHO'S NAMES START WITH "bulky" or "jitr-" they will be also deleted. In case of doubt delete the resources manually!**

	clean-up.py

* Delete the remaining resources manually

		# disable indexing
		aws iot update-indexing-configuration \
  		  --thing-indexing-configuration thingIndexingMode=OFF
		
		# delete the IoT topic rule
		aws iot delete-topic-rule --rule-name JITRRule

		# delete the lambda function
		aws lambda delete-function --function-name jitr

		# empty your S3 bucket. If the bucket is not empty deleting the CloudFormation stack will fail
		aws s3 rm s3://$S3_BUCKET --include "*" --recursive
		
		# delete thing group
		aws iot delete-thing-group --thing-group-name bulk-group
		
		# delete the smart building policy
		aws iot delete-policy --policy-name SmartBuilding_Policy
		
		# get CA certificate id
		aws iot list-ca-certificates
		
		# inactivate CA
		aws iot update-ca-certificate \
		  --new-status INACTIVE --certificate-id [YOUR_CA_CERTIFICATE_ID]
		
		# delete CA
		aws iot delete-ca-certificate \
		  --certificate-id [YOUR_CA_CERTIFICATE_ID]
		
		# deprecation of thing-type needs 5min. If this command is not successful, wait and try again
		aws iot delete-thing-type --thing-type-name bulk-type

		
* If there are any remaining resources like things, certificates, policies, etc. delete them manually

* Detach all remaining certificates from the IoT policy *$IOT_POLICY*
		
* Go to the AWS CloudFormation console

		Delete the stack IoTDeviceManagementWS








 



