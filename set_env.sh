# Export environment variables on local development

export $(grep -v '^#' .env | xargs -d '\n')
