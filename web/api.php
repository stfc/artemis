<?php

if(isset($_REQUEST["list_nodes"])) {
  system("cd ..; ./artemis_cli.py list_nodes --format json");
}
elseif(isset($_REQUEST["list_probes"])) {
  system("cd ..; ./artemis_cli.py list_probes --format json");
}

?>
