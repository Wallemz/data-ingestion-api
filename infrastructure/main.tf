provider "azurerm" {
  features {}
  subscription_id = var.subscription_id  # Pass the subscription ID
}

# Resource Group declaration
resource "azurerm_resource_group" "rg" {
  name     = "rg-data-ingestion"
  location = "East US"
}

# Azure Service Plan (with required os_type and sku_name)
resource "azurerm_service_plan" "app_service_plan" {
  name                = var.serverfarms_ASP_dataingestionproject_9842_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "Y1"  # Corresponds to the "Dynamic" tier for Consumption plan
}

# Azure Linux Function App (with a minimal site_config block)
resource "azurerm_linux_function_app" "function_app" {
  name                = var.sites_fa_data_ingestion_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.app_service_plan.id
  storage_account_name = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME    = "python"
    PYTHON_VERSION              = "3.11"
    AzureWebJobsStorage         = azurerm_storage_account.sa.primary_connection_string
    SERVICE_BUS_CONNECTION_STRING = var.service_bus_connection_string
  }
  
  site_config {
    # This is required but can be left minimal
    always_on = true  # Necessary for premium/consumption plans
  }

  https_only = true
}

# Storage Account
resource "azurerm_storage_account" "sa" {
  name                     = var.storageAccounts_dataingestionprojec81d5_name
  resource_group_name       = azurerm_resource_group.rg.name
  location                  = azurerm_resource_group.rg.location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  min_tls_version           = "TLS1_2"
}

# CosmosDB Account
resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = var.databaseAccounts_data_ingestion_project_db_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }
  
  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}

# Service Bus Namespace
resource "azurerm_servicebus_namespace" "sb_namespace" {
  name                = var.namespaces_sb_data_ingestion_project_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
}

# Service Bus Topic
resource "azurerm_servicebus_topic" "sb_topic" {
  name           = "data-ingestion-topic"
  namespace_id   = azurerm_servicebus_namespace.sb_namespace.id
}

# Service Bus Subscription (with max_delivery_count added)
resource "azurerm_servicebus_subscription" "sb_subscription" {
  name                = "ingestion-handler-subscription"
  topic_id            = azurerm_servicebus_topic.sb_topic.id
  max_delivery_count  = 10  # Maximum delivery attempts before dead-lettering
}

# Variables declaration
variable "subscription_id" {
  type = string
}

variable "sites_fa_data_ingestion_name" {
  type        = string
  default     = "fa-data-ingestion"
}

variable "storageAccounts_dataingestionprojec81d5_name" {
  type        = string
  default     = "dataingestionprojec81d5"
}

variable "databaseAccounts_data_ingestion_project_db_name" {
  type        = string
  default     = "data-ingestion-project-db"
}

variable "namespaces_sb_data_ingestion_project_name" {
  type        = string
  default     = "sb-data-ingestion-project"
}

variable "serverfarms_ASP_dataingestionproject_9842_name" {
  type        = string
  default     = "ASP-dataingestionproject-9842"
}

variable "service_bus_connection_string" {
  type = string
}
