param workspaceName string
param location string
param workbookSourceId string

@description('First observed OperationName string for the role assignment detection.')
param roleAssignmentOperation1 string

@description('Second observed OperationName string for the role assignment detection.')
param roleAssignmentOperation2 string

@description('First observed OperationName string for the service principal credential detection.')
param servicePrincipalCredentialOperation1 string

@description('Second observed OperationName string for the service principal credential detection.')
param servicePrincipalCredentialOperation2 string

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

var failedSigninQuery = loadTextContent('../../kql/analytics/failed_signin_burst_by_ip.kql')

var roleAssignmentQuery = replace(
  replace(
    loadTextContent('../../kql/analytics/directory_role_assignment_change.kql'),
    '<ROLE_ASSIGNMENT_OPERATION_1>',
    roleAssignmentOperation1
  ),
  '<ROLE_ASSIGNMENT_OPERATION_2>',
  roleAssignmentOperation2
)

var spCredentialQuery = replace(
  replace(
    loadTextContent('../../kql/analytics/service_principal_credential_addition.kql'),
    '<SP_CREDENTIAL_OPERATION_1>',
    servicePrincipalCredentialOperation1
  ),
  '<SP_CREDENTIAL_OPERATION_2>',
  servicePrincipalCredentialOperation2
)

resource failedSigninRule 'Microsoft.SecurityInsights/alertRules@2025-09-01' = {
  name: guid(workspace.id, 'lab06-failed-signin-burst-by-ip')
  scope: workspace
  kind: 'Scheduled'
  properties: {
    displayName: 'LAB06 - Failed sign-in burst by IP'
    description: 'Detect repeated failed Entra sign-ins from one IP across multiple users inside a short time window.'
    enabled: true
    query: failedSigninQuery
    queryFrequency: 'PT15M'
    queryPeriod: 'PT15M'
    severity: 'Medium'
    suppressionEnabled: false
    suppressionDuration: 'PT1H'
    tactics: [
      'CredentialAccess'
    ]
    techniques: [
      'T1110'
    ]
    triggerOperator: 'GreaterThan'
    triggerThreshold: 0
    entityMappings: [
      {
        entityType: 'Account'
        fieldMappings: [
          {
            identifier: 'Name'
            columnName: 'FirstUserName'
          }
          {
            identifier: 'UPNSuffix'
            columnName: 'FirstUserUPNSuffix'
          }
        ]
      }
      {
        entityType: 'IP'
        fieldMappings: [
          {
            identifier: 'Address'
            columnName: 'IPAddress'
          }
        ]
      }
    ]
    customDetails: {
      FailureCount: 'FailureCount'
      FailedUsersCount: 'FailedUsersCount'
      FailedUsers: 'FailedUsers'
      AppDisplayNames: 'AppDisplayNames'
    }
    eventGroupingSettings: {
      aggregationKind: 'SingleAlert'
    }
    incidentConfiguration: {
      createIncident: true
      groupingConfiguration: {
        enabled: true
        reopenClosedIncident: false
        lookbackDuration: 'PT1H'
        matchingMethod: 'AllEntities'
        groupByEntities: []
        groupByAlertDetails: []
        groupByCustomDetails: []
      }
    }
  }
}

resource roleAssignmentRule 'Microsoft.SecurityInsights/alertRules@2025-09-01' = {
  name: guid(workspace.id, 'lab06-directory-role-assignment-change')
  scope: workspace
  kind: 'Scheduled'
  properties: {
    displayName: 'LAB06 - Directory role assignment change'
    description: 'Detect Entra directory role assignment or role membership changes.'
    enabled: true
    query: roleAssignmentQuery
    queryFrequency: 'PT1H'
    queryPeriod: 'PT1H'
    severity: 'High'
    suppressionEnabled: false
    suppressionDuration: 'PT1H'
    tactics: [
      'Persistence'
      'PrivilegeEscalation'
    ]
    techniques: [
      'T1098'
    ]
    triggerOperator: 'GreaterThan'
    triggerThreshold: 0
    entityMappings: [
      {
        entityType: 'Account'
        fieldMappings: [
          {
            identifier: 'Name'
            columnName: 'ActorName'
          }
          {
            identifier: 'UPNSuffix'
            columnName: 'ActorUPNSuffix'
          }
        ]
      }
    ]
    customDetails: {
      OperationName: 'OperationName'
      TargetDisplayName: 'TargetDisplayName'
      TargetType: 'TargetType'
      CorrelationId: 'CorrelationId'
    }
    eventGroupingSettings: {
      aggregationKind: 'SingleAlert'
    }
    incidentConfiguration: {
      createIncident: true
      groupingConfiguration: {
        enabled: true
        reopenClosedIncident: false
        lookbackDuration: 'PT1H'
        matchingMethod: 'AllEntities'
        groupByEntities: []
        groupByAlertDetails: []
        groupByCustomDetails: []
      }
    }
  }
}

resource spCredentialRule 'Microsoft.SecurityInsights/alertRules@2025-09-01' = {
  name: guid(workspace.id, 'lab06-service-principal-credential-addition')
  scope: workspace
  kind: 'Scheduled'
  properties: {
    displayName: 'LAB06 - Service principal credential addition'
    description: 'Detect the addition of a new password credential to a service principal.'
    enabled: true
    query: spCredentialQuery
    queryFrequency: 'PT1H'
    queryPeriod: 'PT1H'
    severity: 'High'
    suppressionEnabled: false
    suppressionDuration: 'PT1H'
    tactics: [
      'Persistence'
    ]
    techniques: [
      'T1098.001'
    ]
    triggerOperator: 'GreaterThan'
    triggerThreshold: 0
    entityMappings: [
      {
        entityType: 'Account'
        fieldMappings: [
          {
            identifier: 'Name'
            columnName: 'ActorName'
          }
          {
            identifier: 'UPNSuffix'
            columnName: 'ActorUPNSuffix'
          }
        ]
      }
    ]
    customDetails: {
      OperationName: 'OperationName'
      TargetDisplayName: 'TargetDisplayName'
      TargetType: 'TargetType'
      CorrelationId: 'CorrelationId'
    }
    eventGroupingSettings: {
      aggregationKind: 'SingleAlert'
    }
    incidentConfiguration: {
      createIncident: true
      groupingConfiguration: {
        enabled: true
        reopenClosedIncident: false
        lookbackDuration: 'PT1H'
        matchingMethod: 'AllEntities'
        groupByEntities: []
        groupByAlertDetails: []
        groupByCustomDetails: []
      }
    }
  }
}

resource identityAutomation 'Microsoft.SecurityInsights/automationRules@2025-09-01' = {
  name: guid(workspace.id, 'lab06-identity-incident-triage')
  scope: workspace
  properties: {
    displayName: 'LAB06 - Identity incident triage labeling'
    order: 100
    triggeringLogic: {
      isEnabled: true
      triggersOn: 'Incidents'
      triggersWhen: 'Created'
      conditions: [
        {
          conditionType: 'Property'
          conditionProperties: {
            operator: 'StartsWith'
            propertyName: 'IncidentTitle'
            propertyValues: [
              'LAB06 -'
            ]
          }
        }
      ]
    }
    actions: [
      {
        order: 1
        actionType: 'ModifyProperties'
        actionConfiguration: {
          status: 'Active'
          severity: ''
          classification: ''
          classificationReason: ''
          classificationComment: ''
          labels: [
            {
              labelName: 'lab06-identity'
            }
          ]
        }
      }
    ]
  }
}

resource deployedWorkbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(resourceGroup().id, workspaceName, 'lab06-deployed-workbook')
  location: location
  kind: 'shared'
  properties: {
    category: 'workbook'
    displayName: 'LAB06 - Deployed identity content workbook'
    description: 'Lightweight shared workbook deployed to the test Sentinel workspace for Lab 06.'
    serializedData: loadTextContent('workbook.serialized.json')
    sourceId: workbookSourceId
    version: 'Notebook/1.0'
  }
}