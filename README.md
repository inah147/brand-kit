# Brand Kit Inah

Repositório de identidade visual do grupo Inah. Reúne o manual da marca, cores, tipografia, logotipos, ícones e materiais de referência dos Escoteiros do Brasil.

![Idioma: português do Brasil](https://img.shields.io/badge/idioma-pt--BR-1D2756)
![Formatos: PDF, HTML, PNG e SVG](https://img.shields.io/badge/formatos-PDF%20%7C%20HTML%20%7C%20PNG%20%7C%20SVG-16794A)

## Acesso rápido

- [Manual de Identidade Visual Inah (PDF)](Manual%20de%20Identidade%20Visual%20Inah.pdf)
- [Manual de identidade visual (HTML)](manual-identidade-visual/index.html)
- [Paletas e cores (YAML)](colors.yaml)
- [Tipografia (YAML)](typographi.yaml)
- [Logotipos e marcas](logos/)
- [Manuais de referência dos Escoteiros do Brasil](manuais%20de%20identidade%20visual%20escoteiros%20do%20brasil/)

## Conteúdo

| Caminho | Descrição |
| --- | --- |
| `Manual de Identidade Visual Inah.pdf` | Manual da identidade visual do grupo Inah. |
| `manual-identidade-visual/index.html` | Versão HTML do manual, com referências de cores e aplicações da identidade. |
| `colors.yaml` | Cores da marca Inah, escala de cinza, cores dos ramos e referências dos Escoteiros do Brasil. |
| `typographi.yaml` | Famílias tipográficas e seus usos. |
| `logos/inah/` | Logotipos e aplicações da marca Inah. |
| `logos/ramos/` | Marcas dos ramos escoteiros. |
| `logos/escoteiros do brasil/` | Logotipos dos Escoteiros do Brasil. |
| `manual-identidade-visual/icones/` | Ícones em PNG e SVG, incluindo variações de cor. |
| `manual-identidade-visual/img/` | Imagens utilizadas pelo manual HTML. |
| `manual-identidade-visual/fonte/` | Template, gerador do manual e utilitários em Python. |
| `manuais de identidade visual escoteiros do brasil/` | Documentos de referência em PDF. |

## Visualizar e gerar o manual

Abra `manual-identidade-visual/index.html` em um navegador. Para gerar novamente esse arquivo a partir do template, use Python 3:

```bash
python3 manual-identidade-visual/fonte/build.py \
	manual-identidade-visual/fonte/template.html \
	manual-identidade-visual/index.html
```

O comando usa apenas Python e os módulos do próprio projeto; ele substitui o arquivo HTML de saída indicado no segundo argumento. Para visualizar os documentos PDF, use um leitor de PDF.

## GitHub Pages

O workflow [Deploy GitHub Pages](.github/workflows/pages.yml) publica o manual HTML e seus diretórios de imagens e ícones sempre que há um push para `main`. Depois do primeiro deploy, a página ficará disponível em:

<https://inah147.github.io/brand-kit/>

O workflow tenta ativar o GitHub Pages automaticamente. Se a publicação não iniciar, confira em **Settings > Pages** se a fonte está definida como **GitHub Actions**. O site contém apenas o manual HTML e os recursos necessários; os PDFs e arquivos-fonte continuam no repositório, mas não são publicados como parte do site.

## Uso e direitos

O repositório não declara uma licença de uso. A presença de arquivos aqui não concede, por si só, autorização para redistribuir ou utilizar marcas, logotipos e documentos de terceiros. Antes de publicar, adaptar ou usar esses materiais fora do contexto previsto, confirme as permissões e orientações dos respectivos titulares e consulte os manuais de identidade aplicáveis.

## Tópicos

`brand-kit` · `identidade-visual` · `design-system` · `escotismo` · `logos` · `manual-de-marca`
