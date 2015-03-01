Dockerfile for testing LLVM/zorg builders

Instructions
============

1. Get Docker.
2. Clone this repository.
3. Copy an up-to-date "zorg" tree into this directory from the LLVM svn
   repo, if the included one does not suffice.
4. Update config/builders.py and master.cfg with any desired changes to
   add schedulers, builders, etc.
5. Build Docker image: "docker build -t zorg ."
6. Run the image: "docker run -d -p 8010:8010 -p 22 zorg"

You should now be able to test builders by navigating to the builders
and forcing builds, or waiting for the poller to detect source changes.

