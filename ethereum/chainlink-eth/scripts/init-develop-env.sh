CURRENT_DIR=$(pwd)
PROJECT_DIR="$(dirname "$CURRENT_DIR")"


if ! [ -x "$(command -v python)" ]; then
  echo 'Error: python is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v poetry)" ]; then
  echo 'Warning: python-poetry is not installed in global environment, try installing via pip...'
  pip install poetry==1.4.0
fi


cat > ../.env <<EOF
AWS_ACCESS_KEY_ID=IKIDJXwOittgOxRnvrolgT9nLCqRuPjwuofW
AWS_SECRET_ACCESS_KEY=pSq10mRsCKrBLKAoIcmzESaYs5B4nKhw
CHAINMODELING_NETWORK=mainnet
CHAINMODELING_DATALAKE_ENDPOINT=https://datalake-kaya-dev-1316492204.cos.ap-singapore.myqcloud.com
CHAINMODELING_CHAINLAKE_ENDPOINT=http://chainlake-tencent-dev.cao365.io
CHAINMODELING_CLICKHOUSE_HOST=clickhouse.dev.kaya
CHAINMODELING_CLICKHOUSE_USER=chainmodeling
CHAINMODELING_CLICKHOUSE_PASS='0059*3yiRftD'
CHAINMODELING_VERSION=
CHAINMODELING_NETWORK=
DBT_PROFILES_DIR=$DBT_PROFILES_DIR/
DBT_PROJECT_DIR=$PROJECT_DIR/ddl/
PREFECT_API_URL=http://jobengine.dev.kaya/api
EOF

poetry self add poetry-dotenv-plugin
poetry self add 'poethepoet[poetry_plugin]'
poetry env use python3.9
cd ..
poetry install --with dev,test --sync


  echo "\


██╗  ██╗ █████╗ ██╗   ██╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗
█████╔╝ ███████║ ╚████╔╝ ███████║
██╔═██╗ ██╔══██║  ╚██╔╝  ██╔══██║
██║  ██╗██║  ██║   ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  

Done. Please run dbt commands in the project root directory.       
"
