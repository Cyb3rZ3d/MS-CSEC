***Ruben Valdez*** <br>
CSCI/CSEC 5372 | Cloud Computing | Thursdays @ 4pm<br>
Prof. Yang, Jeong <br>
Project Assignment 1: Lab 2<br>
Due by Sunday midnight, October 12, 2025

---

<br><br>


```
Some Jooli Inc. standards you should follow:

- Create all resources in the REGION region and ZONE zone, unless otherwise directed.
- Use the project VPCs.
- Naming is normally team-resource, e.g. an instance could be named kraken-webserver1.
- Allocate cost effective resource sizes. Projects are monitored and excessive resource use will result in the containing project's termination (and possibly yours), so beware. This is the guidance the monitoring team is willing to share: unless directed, use e2-medium.
```



# Task 1. Create development VPC manually

1. Open cloud shell

gcloud auth list

gcloud config set project qwiklabs-gcp-01-e94661b16edf

gcloud config set compute/region us-west1

gcloud config set compute/zone us-west1-a

export REGION=us-west1
export ZONE=us-west1-a
echo $REGION
echo $ZONE

gcloud compute networks create griffin-dev-vpc \
--subnet-mode=custom

![alt text](image-10.png)

![alt text](image-9.png)




# Task 2. Create production VPC manually

![alt text](image-11.png)

![alt text](image-12.png)


# Task 3. Create bastion host


![alt text](image-14.png)

![alt text](image-15.png)




# Task 4. Create and configure Cloud SQL Instance

![alt text](image-16.png)  

![alt text](image-17.png)


# Task 5. Create Kubernetes cluster


![alt text](image-18.png)

![alt text](image-19.png)


# Task 6. Prepare the Kubernetes cluster

![alt text](image-20.png)

![alt text](image-21.png)





# Task 7. Create a WordPress deployment

![alt text](image-23.png)
![alt text](image-22.png)



# Task 8. Enable monitoring

![alt text](image-28.png)

![alt text](image-24.png)



# Task 9. Provide access for an additional engineer

![alt text](image-26.png)

![alt text](image-27.png)