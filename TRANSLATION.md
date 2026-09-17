# Translation Guidelines for Poliedros

Welcome to the **Poliedros** translation guide.

## Translation Philosophy & Sentence Structure

In our codebase, you may notice complete sentences containing formatted variables:

```python
# Translators: "Explode" and "in" are the only words to translate.
# The tags %(sel)s, %(child)s, %(kept)s, and %(total)s are code variables and must remain intact.
_("Explode %(sel)s in %(child)s → %(kept)s = %(total)s")
```

### Why Do We Keep Full Sentences?
We deliberately preserve complete sentences with variable placeholders rather than chopping strings into smaller fragments (e.g., translating "Explode" and "in" separately).

* **Grammatical Flexibility:** Languages structure sentences differently. For example, in German or Russian, verb placement, noun gender, and prepositions often depend on the context of the whole phrase.
* **Natural Flow:** Concatenating isolated translated words often results in unnatural or grammatically broken sentences in non-English languages.

## Guidelines for Translators

When working with .pot / .po files (via text editor, Poedit, Weblate, Transifex, etc.):

1. **Read Code Comments (#. Translators:):** Look above the msgid in .pot files for contextual notes detailing which words need translation and which tags represent values.
2. **Preserve Variable Tags Exactly:** Do not alter, translate, or remove placeholders like %(sel)s, %(child)s, %(kept)s, or %(total)s.
3. **Adapt Word Order as Needed:** Reorder the variables and words to fit the natural grammar and syntax of your target language.

### Example

**Source String:**

```
#. Translators: "Explode" and "in" are the only words to translate.
#. The tags %(sel)s, %(child)s, %(kept)s, and %(total)s are variables and must remain intact.
#: poliedros/dice.py:42
msgid "Explode %(sel)s in %(child)s → %(kept)s = %(total)s"
msgstr ""
```

**Portuguese (pt-BR):**

```
msgstr "Explodir %(sel)s em %(child)s → %(kept)s = %(total)s"
```

## Translation Workflow & How to Contribute

To contribute a new language or update an existing translation using `.pot` and `.po` files, follow these steps:

### 1. Tools You Can Use
You can edit translation files using dedicated GUI tools or plain text editors:
* **Poedit** (Recommended – free, cross-platform tool specifically designed for Gettext `.po` files)
* **Weblate** or **Transifex** (if hosted online)
* Any text editor (VS Code, Sublime Text, Vim, etc.)

---

### 2. Creating or Updating a Translation

#### A. Translating an Existing Language

1. Locate the `.po` file for your language inside the `po/` directory (e.g., `po/pt_BR.po`).
2. Open the file in **Poedit** (or your text editor).
3. If new strings were added to Poliedros, sync your `.po` file with the main template:
   * In **Poedit**, go to **Catalog → Update from POT file...** and select `po/poliedros.pot`.
4. Translate or update the untranslated and fuzzy strings.
5. Save the file.

#### B. Adding a Brand New Language
1. Copy the template file `locale/poliedros.pot` to create a new `.po` file inside the corresponding language folder:

```bash
mkdir -p locale/<lang_code>/LC_MESSAGES/
cp locale/poliedros.pot locale/<lang_code>/LC_MESSAGES/poliedros.po
```

*(Replace `<lang_code>` with the ISO language code, e.g., `es` for Spanish, `fr` for French).*
2. Open the new `poliedros.po` in Poedit or your text editor.
3. Translate all `msgstr` entries.

---

### 4. Registering the New Language

If you are adding a new language, register its language code the `po/LINGUAS` file:

1. Open `po/LINGUAS` in a text editor.
2. Add your language code on a new line (in alphabetical order):

```
# Please keep this file sorted alphabetically.
de
pt_BR
ru_RU
```

### 5. Submitting Your Contribution

1. Commit your new/updated `.po` file in `po/` and the updated `po/LINGUAS` file (if adding a language).
2. Push your changes to your GitHub fork.
3. Open a **Pull Request (PR)** with a title like:
   * `i18n: Add <Language Name> translation`
   * `i18n: Update <Language Name> translation`

## Developer Note: Extracting Comments to .pot

When generating or updating the .pot template, always include the -c flag with xgettext so comments starting with Translators: are exported properly:

```bash
xgettext -c="Translators:" --keyword=_ -o locale/poliedros.pot *.py
```