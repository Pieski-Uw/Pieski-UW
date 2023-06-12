#!/bin/bash

cat pieski_pet.backup | psql -U postgres
cat pieski_pet_seq.backup | psql -U postgres