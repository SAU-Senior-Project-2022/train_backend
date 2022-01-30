**Backend Requirements:**

_FUNCTIONAL:_
1. The backend shall provide a way for all train station sensor modules a way to connect to the server using http.
2. The backend shall provide the frontend REST endpoints to give end users the most up-to-date information about the relevant train stations.

_NON-FUNCTIONAL:_
1. The backend shall be capable of hosting multiple connections (up to 3). The server is not multi-threaded thus it is not actually simultaneous. 
2. The backend shall provide multiple possible endpoints to provide the frontend and hardware a variety of API calls.
3. The backend shall store the data that has been provided in the database.
4. The backend shall give a respose in less than 3 seconds.
5. The backend shall use the following:
     - Docker-Compose
     - Git (both 2.35.0 and 2.25.1 have been tested to work)
     - Docker (most of the other items will be installed if you're going alone this route)
     - Sqlite (both 3.31.1 and 3.37.2 have been tested to work)
     - Python 3.10.2
     - Flask  2.0.2 (pip installation) 
     - cryptography 36.0.1 (pip installation)
     - argparse 1.4.0(pip installation)

_LIMITATIONS:_
Due to limited time, we are declaring the following items out of scope for this sprint: 
- connection security/authentication
- Error handling with less than perfect input
- User authentication

![UML Use Case DIagram](https://github.com/SAU-Senior-Project-2022/train_backend/blob/master/usecase.svg?raw=true)
