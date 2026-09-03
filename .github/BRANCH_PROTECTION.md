# Schutz für `main`

Nach dem ersten Push in GitHub unter **Settings → Branches → Add branch
protection rule** für `main` aktivieren:

- Pull Request vor dem Merge verlangen.
- Mindestens eine Freigabe verlangen.
- Veraltete Freigaben bei neuen Commits zurücksetzen.
- Statuschecks vor dem Merge verlangen und als erforderlich markieren:
  `Python quality (3.11)`.
- Direkte Pushes und Force-Pushes auf `main` sperren.
- Bei einer GitHub-Organisation: Code-Owner-Review aktivieren und
  `.github/CODEOWNERS` mit dem tatsächlichen Team ergänzen.

Die Regel selbst ist eine GitHub-Repositoryeinstellung und kann nicht durch
eine Datei im Repository erzwungen werden. Diese Datei dokumentiert die
verbindliche Zielkonfiguration.
