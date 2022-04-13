## smartphone-servers
Project Landing Page: https://github.com/jfswitzer/The_Renee_Project/wiki

## How to run a simple test (on a single machine)

1. Open three tabs

2. In tab #1:

```cd conductor``` \
```./run_conductor.sh```

This starts the management client.

3. In tab #2

```cd phones``` \
```./run_client.sh```

This starts one client process; you can start more, for more complex testing.

4. In tab #3

```cd tests``` \
```./tests.sh```

This sends a single task. You can send more once it completes.
