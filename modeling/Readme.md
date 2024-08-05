
# Data Collection

## Requirements

NVIDIA [Cuda GPU drivers](...) for the host machine (optional).
Firebase [account and project with Firebase Storage](...) configured.

https://firebase.google.com/docs/storage/admin/start

## Instructions

Move and rename the file into `/Dataset/private/serviceAdmin.json`

Create `.env` next to the `Dockerfile` with the following configuration:

```dotenv
FIREBASE_STORAGE_BUCKET=<name of your firebase storage bucket, default is the name of your project (see image, without the gs:// and without the appspot.com)>
```