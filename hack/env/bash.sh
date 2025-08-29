set -o errexit
set -o nounset
set -o pipefail

debug="${DEBUG:-}"

if [[ "${debug,,}" = true || "${debug}" = 1 ]];
then
  set -o xtrace
fi
