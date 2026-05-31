# 🚀 Deploy no Vercel

## Opção 1: Deploy Automático (Recomendado)

1. Acesse: https://vercel.com/new
2. Conecte sua conta GitHub (vfcolares-lab)
3. Selecione o repositório: `dashboard-2026-parana`
4. Vercel detecta automaticamente o projeto
5. Clique em "Deploy"
6. Pronto! ✅

## Opção 2: Deploy via CLI (se instalado)

```bash
vercel --prod
```

## Resultado

Seu dashboard estará online em:
- **URL Principal:** https://dashboard-2026-parana.vercel.app
- **URL GitHub:** https://github.com/vfcolares-lab/dashboard-2026-parana

## Estrutura do Deploy

```
/
├── index.html          → Dashboard principal
├── secoes_2022.js      → Dados (20.232 seções)
├── vercel.json         → Configuração
└── data/
    ├── secoes_2022.json
    └── secoes_2022.js
```

O Vercel serve o `index.html` como arquivo estático. Todos os dados já estão inline no arquivo.
