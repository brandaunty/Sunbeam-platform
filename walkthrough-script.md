# 3-minute walkthrough script

Counts measured: Docker 3 commands, Dokku 4 commands.

## 0:00-0:30 On camera: the user and the three decisions
"The primary user is the field revenue officer at Sunbeam: someone on a phone, assigned to a set of feeders, visiting customers to report tampering, bypass and wrong mapping. The platform serves three decisions. One: which feeders should field teams visit this month, decided by the head of revenue protection. Two: is there an outage on a feeder right now, decided by the network controller within fifteen minutes. Three: is this estimated bill justified and can this disconnection be reviewed, decided by the billing dispute officer. If a component doesn't serve one of these, it doesn't belong."

## 0:30-1:10 Screen: VirtualBox estate
- Show VirtualBox with your VMs running (for example `docker-host`, `dokku-host`, and the `keyserver` VM for Abeokuta).
- Say: "This is my estate. Three VMs: one for Docker, one for Dokku, one standing in for the key server in Abeokuta."

## 1:10-1:50 Screen: Docker
```
docker build -t sunbeam-field .
docker run -d -p 5000:5000 sunbeam-field
curl localhost:5000/health
```
Say: "Docker: 3 commands. I control the image and how it runs, which gives portability but I do the plumbing."

## 1:50-2:30 Screen: Dokku
```
dokku apps:create sunbeam-field        # on the Dokku host
git remote add dokku dokku@localhost:sunbeam-field
git push dokku main
curl -H "Host: sunbeam-field.dokku-host" localhost:5000/health
```
Say: "Dokku: 4 commands. Push the code and the platform builds, routes and restarts. That is the PaaS model, and it is right for the dashboard and pipeline because we have no platform engineer."

## 2:30-2:50 Screen: reasoning on service models
"Pipeline: PaaS. Lake and query: managed. Outage alert: FaaS. Assistant: SaaS. Key service: infrastructure I control."

## 2:50-3:00 On camera: the workload I refused to move
"The one workload I refused to move is the re-identification key service. It is the only thing that turns pseudonymous readings back into named households, and consumption patterns reveal when people are home. It stays on a server we control in Abeokuta, so a cloud incident cannot expose anyone's identity."
