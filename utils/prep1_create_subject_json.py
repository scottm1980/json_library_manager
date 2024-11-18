from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI()

# User input
user_input = "\n\nCrossword App flutter dart iOS & Android\n\n"

# Make OpenAI API request

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
   {
            "role": "system",
            "content": "I am a technical writer and as such, I excel in clear, concise communication, skillfully breaking down complex technical concepts for a variety of code bases. My proficiency in research and attention to detail ensures accuracy and consistency in my work. I adeptly collect and organize complex information in an efficient manner, understanding and anticipating the needs of the app. In my role, I always prioritize optimized plans for future development."
        },
        {
            "role": "system",
            "content": "I will meticulously research and compile a 5-page report focused on the 'user_input'. I will then use the contents of my report to compile a detailed response."
        },
        {
            "role": "assistant",
            "content": "This is the first and foundational step in the process for generating a high-fidelity production app. I must therefore be precise and complete."
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
    temperature=1.4,
    max_tokens=5000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "json_schema",
        "json_schema": {
      "name": "app_plan",
      "strict": True,
      "schema": {
        "type": "object",
        "properties": {
          "subject": {
            "type": "string",
            "description": "The subject or main focus of the app."
          },
          "details": {
            "type": "string",
            "description": "Additional details regarding the app."
          },
          "requirements": {
            "type": "object",
            "properties": {
              "flutter": {
                "type": "object",
                "properties": {
                  "codePatternRecommendation": {
                    "type": "string",
                    "description": "Recommended code patterns for Flutter 3.24.3 development."
                  },
                  "dart": {
                    "type": "object",
                    "properties": {
                      "version": {
                        "type": "string",
                        "description": "Using Dart sdk 3.5.4. and Flutter 3.24.4."
                      },
                      "guidelines": {
                        "type": "string",
                        "description": "Guidelines for Dart development."
                      },
                    },
                    "required": [
                      "version",
                      "guidelines"
                    ],
                    "additionalProperties": False
                  },               
                  "android": {
                    "type": "object",
                    "properties": {
                      "version": {
                        "type": "string",
                        "description": "Android 34, min 32. Material design requirements."
                      },
                      "guidelines": {
                        "type": "string",
                        "description": "Dart converts to native Android code."
                      }
                    },
                    "required": [
                      "version",
                      "guidelines"
                    ],
                    "additionalProperties": False
                  },
                  "ios": {
                    "type": "object",
                    "properties": {
                      "version": {
                        "type": "string",
                        "description": "iOS version 18, min 16. Cupertino design requirements."
                      },
                      "guidelines": {
                        "type": "string",
                        "description": "Dart converts to native iOS code."
                      }
                    },
                    "required": [
                      "version",
                      "guidelines"
                    ],
                    "additionalProperties": False
                  }
                },
                "required": [
                  "codePatternRecommendation",
                  "dart",
                  "android",
                  "ios"
                ],
                "additionalProperties": False
              }
            },
            "required": [
              "flutter"
            ],
            "additionalProperties": False
          },
          "features": {
            "type": "object",
            "properties": {
              "appSpecific": {
                "type": "string",
                "description": "Features specific to this app."
              },
              "user": {
                "type": "string",
                "description": "User-related features."
              },
              "soloPlay": {
                "type": "boolean",
                "description": "Indicates if the app has online functionality. If false then the app is a solo play app, with no leaderboards, messaging, or other 'online' features."
              },
              "pushNotifications": {
                "type": "boolean",
                "description": "Indicates if the app supports push notifications."
              }
            },
            "required": [
              "appSpecific",
              "user",
              "soloPlay",
              "pushNotifications"
            ],
            "additionalProperties": False
          },
          "design": {
            "type": "object",
            "properties": {
              "screens": {
                "type": "array",
                "description": "Think through the entire app lifecycle, from start to finish, and list the screens that players interact with at each stage.",
                "items": {
                  "type": "string"
                }
              },
              "theme": {
                "type": "object",
                "properties": {
                  "colors": {
                    "$ref": "#/$defs/Color"
                  },
                  "typography": {
                    "$ref": "#/$defs/Typography"
                  }
                },
                "required": [
                  "colors",
                  "typography"
                ],
                "additionalProperties": False
              }
            },
            "required": [
              "screens",
              "theme"
            ],
            "additionalProperties": False
          },
          "backend": {
            "type": "object",
            "properties": {
              "firebaseRecommended": {
                "type": "boolean",
                "description": "Which Firebase is recommended for the backend."
              },
              "thirdPartyServices": {
                "type": "array",
                "description": "List of third-party services to be used.",
                "items": {
                  "type": "string"
                }
              },
              "apiIntegrations": {
                "type": "array",
                "description": "Preferable none, as Firebase is backend.",
                "items": {
                  "type": "string"
                }
              },
              "cloudStorageRequirements": {
                "type": "string",
                "description": "Requirements for cloud storage."
              },
              "databaseRequirements": {
                "type": "string",
                "description": "Requirements for the database."
              }
            },
            "required": [
              "firebaseRecommended",
              "thirdPartyServices",
              "apiIntegrations",
              "cloudStorageRequirements",
              "databaseRequirements"
            ],
            "additionalProperties": False
          },
          "development": {
            "type": "object",
            "properties": {
              "frontendRecommendations": {
                "type": "string",
                "description": "Recommendations for frontend development."
              },
              "recommendedPackages": {
                "type": "array",
                "description": "List of recommended packages.",
                "items": {
                  "type": "string"
                }
              },
              "recommendedFrameworks": {
                "type": "array",
                "description": "List of recommended frameworks.",
                "items": {
                  "type": "string"
                }
              },
              "stateManagementPattern": {
                "type": "string",
                "description": "Recommended state management pattern."
              },
              "debuggingAndLogging": {
                "type": "string",
                "description": "Recommendations for debugging and logging."
              },
              "unitAndIntegrationTesting": {
                "type": "string",
                "description": "Approach for unit and integration testing."
              }
            },
            "required": [
              "frontendRecommendations",
              "recommendedPackages",
              "recommendedFrameworks",
              "stateManagementPattern",
              "debuggingAndLogging",
              "unitAndIntegrationTesting"
            ],
            "additionalProperties": False
          },
          "architecture": {
            "type": "object",
            "properties": {
              "designPatterns": {
                "type": "array",
                "description": "List of design patterns used.",
                "items": {
                  "$ref": "#/$defs/DesignPatterns"
                }
              },
              "subSystemDesignPatterns": {
                "type": "array",
                "description": "List of subsystem design patterns used.",
                "items": {
                  "$ref": "#/$defs/DesignPatterns"
                }
              },
              "stateManagementPattern": {
                "type": "string",
                "description": "Description of the state management pattern used."
              },
              "architectureStyle": {
                "$ref": "#/$defs/ArchitectureStyle"
              }
            },
            "required": [
              "designPatterns",
              "subSystemDesignPatterns",
              "stateManagementPattern",
              "architectureStyle"
            ],
            "additionalProperties": False
          },
          "process": {
            "type": "object",
            "properties": {
              "bestPractices": {
                "type": "string",
                "description": "Recommended best practices."
              },
              "continuousIntegrationAndDeployment": {
                "type": "string",
                "description": "Approach to CI/CD."
              },
              "appUpdateStrategy": {
                "type": "string",
                "description": "Strategy for app updates."
              },
              "deploymentTargets": {
                "type": "array",
                "description": "Targets for application deployment.",
                "items": {
                  "$ref": "#/$defs/DeploymentTarget"
                }
              }
            },
            "required": [
              "bestPractices",
              "continuousIntegrationAndDeployment",
              "appUpdateStrategy",
              "deploymentTargets"
            ],
            "additionalProperties": False
          },
          "constraints": {
            "type": "object",
            "properties": {
              "limitations": {
                "type": "string",
                "description": "Any limitations of the app."
              },
              "dataPrivacyCompliance": {
                "type": "string",
                "description": "Data privacy compliance requirements."
              },
              "energyEfficiency": {
                "type": "string",
                "description": "Energy efficiency considerations."
              }
            },
            "required": [
              "limitations",
              "dataPrivacyCompliance",
              "energyEfficiency"
            ],
            "additionalProperties": False
          },
          "responsibilities": {
            "type": "object",
            "properties": {
              "appBloc": {
                "type": "string",
                "description": "Responsibilities related to the app BLoC."
              },
              "serviceLayer": {
                "type": "string",
                "description": "Responsibilities related to the service layer."
              },
              "uiLayer": {
                "type": "string",
                "description": "Responsibilities for the UI layer."
              },
              "dataLayer": {
                "type": "string",
                "description": "Responsibilities for the data layer."
              },
              "authenticationModule": {
                "type": "string",
                "description": "Responsibilities for the authentication module."
              },
              "notificationModule": {
                "type": "string",
                "description": "Responsibilities for the notification module."
              },
              "paymentModule": {
                "type": "string",
                "description": "Responsibilities for the payment module."
              },
              "errorBoundary": {
                "type": "string",
                "description": "Responsibilities for the error boundary."
              }
            },
            "required": [
              "appBloc",
              "serviceLayer",
              "uiLayer",
              "dataLayer",
              "authenticationModule",
              "notificationModule",
              "paymentModule",
              "errorBoundary"
            ],
            "additionalProperties": False
          },
          "strategy": {
            "type": "object",
            "properties": {
              "monetizationStrategies": {
                "type": "string",
                "description": "Strategies for monetization."
              },
              "scalabilityConsiderations": {
                "type": "string",
                "description": "Considerations for scalability."
              },
              "performanceRequirements": {
                "type": "string",
                "description": "Requirements for app performance."
              },
              "securityConsiderations": {
                "type": "string",
                "description": "Considerations for app security."
              },
              "accessibilityRequirements": {
                "type": "string",
                "description": "Requirements for accessibility."
              },
              "localizationAndInternationalization": {
                "type": "string",
                "description": "Requirements for localization and internationalization."
              }
            },
            "required": [
              "monetizationStrategies",
              "scalabilityConsiderations",
              "performanceRequirements",
              "securityConsiderations",
              "accessibilityRequirements",
              "localizationAndInternationalization"
            ],
            "additionalProperties": False
          }
        },
        "$defs": {
          "Color": {
            "type": "object",
            "properties": {
              "primary": {
                "type": "string",
                "description": "Primary color of the app."
              },
              "secondary": {
                "type": "string",
                "description": "Secondary color of the app."
              }
            },
            "required": [
              "primary",
              "secondary"
            ],
            "additionalProperties": False
          },
          "Typography": {
            "type": "object",
            "properties": {
              "fontFamily": {
                "type": "string",
                "description": "Font family used in the app."
              },
              "fontSize": {
                "type": "string",
                "description": "Font size used in the app."
              },
              "fontWeight": {
                "type": "string",
                "description": "Font weight used in the app."
              }
            },
            "required": [
              "fontFamily",
              "fontSize",
              "fontWeight"
            ],
            "additionalProperties": False
          },
          "VersionRequirements": {
            "type": "object",
            "properties": {
              "minimum": {
                "type": "string",
                "description": "Minimum version required."
              },
              "recommended": {
                "type": "string",
                "description": "Recommended version."
              }
            },
            "required": [
              "minimum",
              "recommended"
            ],
            "additionalProperties": False
          },
          "DeploymentTarget": {
            "type": "object",
            "properties": {
              "platform": {
                "type": "string",
                "description": "Platform to deploy the app on."
              },
              "version": {
                "$ref": "#/$defs/VersionRequirements"
              }
            },
            "required": [
              "platform",
              "version"
            ],
            "additionalProperties": False
          },
          "DesignPatterns": {
            "type": "string",
            "description": "Various design patterns that can be referenced."
          },
          "ArchitectureStyle": {
            "type": "string",
            "description": "Description of the architecture style used for the app."
          }
        },
        "required": [
          "subject",
          "details",
          "requirements",
          "features",
          "design",
          "backend",
          "development",
          "architecture",
          "process",
          "constraints",
          "responsibilities",
          "strategy"
        ],
        "additionalProperties": False
      }
    }
  }
)

# Extract the JSON response from the API output
response_content = response.choices[0].message.content

# Convert the response content to a valid JSON object
response_json = json.loads(response_content)

# Save the JSON response to a file
with open('alignment_files/subject.json', 'w') as json_file:
    json.dump(response_json, json_file, indent=4)

print("JSON response saved to subject.json")
