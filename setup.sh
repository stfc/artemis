#!/bin/bash

#
#  Copyright Science and Technology Facilities Council, 2009.
#  
#  This file is part of ARTEMIS.
#  
#  ARTEMIS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  ARTEMIS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with ARTEMIS. If not, see <http://www.gnu.org/licenses/>.
#
#  $Revision$
#  $Date$
#  $LastChangedBy$

DATA_DIR=data
RRD_DIR=rrds
CONFIG_FILE=artemis_config.py
CONFIG_FILE_TEMPLATE=artemis_config.py.template
LOCK_FILE=setup.lock

if [ ! -f $LOCK_FILE ]; then
  echo "INFO: Starting setup"

  if [ ! -e $DATA_DIR ]; then
    echo "INFO: Creating data directory"
    mkdir $DATA_DIR
    touch $LOCK_FILE

    if [ -d $DATA_DIR ]; then
      echo "INFO: Data directory created"

      if [ ! -e $RRD_DIR ]; then
        echo "INFO: Creating RRD directory"
        mkdir $RRD_DIR

        if [ -d $RRD_DIR ]; then
          echo "INFO: RRD directory created"

          if [ ! -e $CONFIG_FILE ]; then
            echo "INFO: Creating stub config file"
            cp $CONFIG_FILE_TEMPLATE $CONFIG_FILE

            if [ -f $CONFIG_FILE ]; then
              echo "INFO: Stub config file sucessfully created"

            else
              echo "ERROR: Creation of stub config file failed"
              exit 1
            fi
          else
            echo "ERROR: Could not create stub config file, as it already exists!"
            exit 1
          fi
        else
          echo "ERROR: Creation of RRD directory failed"
          exit 1
        fi
      else
        echo "ERROR: Could not create RRD directory, as it already exists!"
        exit 1
      fi
    else
      echo "ERROR: Creation of data directory failed"
      exit 1
    fi
  else
    echo "ERROR: Could not create data directory, as it aleady exists!"
    exit 1
  fi
else
  echo "ERROR: Setup has already been run, delete $LOCK_FILE if you are really sure you want it to be re-run!"
  exit 1
fi
