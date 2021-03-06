#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, sys
from utils.file import load_json
from utils.osrm import table

# Parse a json-formatted input instance, compute the matrix using
# OSRM, then add the matrix and all relevant indices to the input
# problem. Possible usage include checking that solving is consistent
# between both instances, or creating a "standalone" problem instance
# that can be further solved even without an OSRM server handy.

def round_to_cost(d):
  return int(d + 0.5)

if __name__ == "__main__":
  input_file = sys.argv[1]
  output_name = input_file[:input_file.rfind('.json')] + '_matrix.json'

  data = load_json(input_file)

  # Retrieve all problem locations in the same order as in
  # input_parser.cpp.
  locs = []

  for v in data['vehicles']:
    if ('start' not in v) and ('end' not in v):
      sys.exit("Missing coordinates for vehicle.")

    if 'start' in v:
      v['start_index'] = len(locs)
      locs.append(v['start'])
    if 'end' in v:
      v['end_index'] = len(locs)
      locs.append(v['end'])

  for job in data['jobs']:
    if ('location' not in job):
      sys.exit("Missing coordinates for job.")
    else:
      job['location_index'] = len(locs)
      locs.append(job['location'])

  # Get table from OSRM.
  matrix = table(locs)['durations']
  data['matrix'] = []

  # Round all costs to the nearest integer (same behavior as in
  # osrm_wrapper.h)
  for line in matrix:
    data['matrix'].append(map(lambda d: round_to_cost(d), line))

  with open(output_name, 'w') as out:
    print 'Writing problem with matrix to ' + output_name
    json.dump(data, out, indent = 2)

