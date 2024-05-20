#!/usr/bin/env bash

make install && psql -a -d postgresql://work:myPassword@localhost:5432/database -f database.sql