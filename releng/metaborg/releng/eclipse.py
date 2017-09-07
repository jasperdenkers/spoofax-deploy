from eclipsegen.preset import Presets

from eclipsegen.generate import EclipseGenerator, EclipseMultiGenerator


class MetaborgEclipseGenerator(object):
  spoofaxRepo = 'http://download.spoofax.org/update/nightly/'
  spoofaxRepoLocal = 'spoofax-eclipse/org.metaborg.spoofax.eclipse.updatesite/target/site'
  spoofaxIUs = ['org.metaborg.spoofax.eclipse.feature.feature.group']
  spoofaxLangDevIUs = [
    'org.metaborg.spoofax.eclipse.meta.feature.feature.group',
    'org.metaborg.spoofax.eclipse.meta.m2e.feature.feature.group'
  ]

  def __init__(self, workingDir, destination, spoofax=True, spoofaxRepo=None, spoofaxRepoLocal=False,
      langDev=True, lwbDev=True, moreRepos=None, moreIUs=None):
    if spoofaxRepoLocal:
      spoofaxRepo = MetaborgEclipseGenerator.spoofaxRepoLocal
    elif not spoofaxRepo:
      spoofaxRepo = MetaborgEclipseGenerator.spoofaxRepo

    if lwbDev:
      langDev = True

    if not moreRepos:
      moreRepos = []
    if not moreIUs:
      moreIUs = []

    presets = [Presets.platform.value, Presets.java.value, Presets.xml.value, Presets.git.value, Presets.maven.value, Presets.gradle.value]
    if langDev or lwbDev:
      presets.extend([Presets.plugin.value, Presets.plugin_maven.value])
    repos, ius = Presets.combine_presets(presets)

    repos.add(spoofaxRepo)
    ius.update(MetaborgEclipseGenerator.spoofaxIUs)
    if langDev or lwbDev:
      ius.update(MetaborgEclipseGenerator.spoofaxLangDevIUs)

    repos.update(moreRepos)
    ius.update(moreIUs)

    self.workingDir = workingDir
    self.destination = destination
    self.repos = repos
    self.ius = ius

  def generate(self, **kwargs):
    generator = EclipseGenerator(self.workingDir, self.destination, repositories=self.repos, installUnits=self.ius,
      **kwargs)
    return generator.generate()

  def generate_all(self, **kwargs):
    generator = EclipseMultiGenerator(self.workingDir, self.destination, repositories=self.repos, installUnits=self.ius,
      **kwargs)
    return generator.generate()
