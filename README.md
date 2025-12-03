# Documentación de Rasa

`````
project/
├── README.md
├── config.yml
├── credentials.yml
├── domain.yml
├── endpoints.yml
├── data/
│   ├── nlu/
│   │   ├── intents/
│   │   │   ├── experiencia.yml
│   │   │   ├── saludos.yml
│   │   │   ├── despedidas.yml
│   │   │   ├── skills.yml
│   │   │   └── smalltalk.yml
│   │   ├── entities/
│   │   │   ├── tecnologia.yml
│   │   │   ├── empresa.yml
│   │   │   └── idiomas.yml
│   │   ├── lookups/
│   │   │   ├── tecnologias.txt
│   │   │   └── empresas.txt
│   │   ├── synonyms/
│   │   │   ├── tecnologia_synonyms.yml
│   │   │   └── empresa_synonyms.yml
│   │   └── regex/
│   │       ├── fechas.yml
│   │       └── numeros.yml
│   ├── rules/
│   │   ├── experiencia_rules.yml
│   │   ├── fallback_rules.yml
│   │   └── saludo_rules.yml
│   ├── stories/
│   │   ├── experiencia_stories.yml
│   │   ├── generales.yml
│   │   └── smalltalk.yml
│   └── tests/
│       ├── nlu/
│       │   └── test_nlu.yml
│       └── stories/
│           └── test_conversaciones.yml
├── actions/
│   ├── __init__.py
│   ├── experienca/
│   │   └── action_experiencia.py
│   ├── empresas/
│   │   └── action_historial_empresas.py
│   ├── validadores/
│   │   └── validate_tecnologias.py
│   ├── forms/
│   │   └── experiencia_form.py
│   ├── utils/
│   │   ├── date_utils.py
│   │   ├── text_utils.py
│   │   └── tecnologia_utils.py
│   ├── constants/
│   │   └── tecnologias_map.py
│   └── data/
│       └── empresas.json
├── tests/
│   ├── unit/
│   │   └── test_experiencia_action.py
│   └── integration/
│       └── test_forms.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
└── .github/
    └── workflows/
        ├── rasa-ci.yml
        ├── rasa-deploy.yml
        └── tests.yml
`````
