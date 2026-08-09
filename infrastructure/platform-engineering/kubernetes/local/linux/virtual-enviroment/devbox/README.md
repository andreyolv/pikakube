[← Virtual environment](../README.md)

# Devbox

<https://github.com/jetify-com/devbox>
<https://github.com/NixOS/nix>
<https://github.com/NixOS/nixpkgs>
<https://www.nixhub.io/>

---

## The problem it solves

Nix guarantees reproducible, isolated environments and asks you to learn a functional language to
get them. Devbox keeps the guarantee and replaces the language with a `devbox.json` listing package
names and versions.

The result: `devbox shell` in a project directory gives you exactly the tools that project declares,
at exactly the declared versions, with nothing installed into the host. Another machine cloning the
repository gets the same environment from the same file. Leaving the shell leaves no trace.

## When to use it

- Different projects need different versions of the same tool
- Onboarding should be "clone, `devbox shell`, work" rather than a wiki page
- You want the host kept clean and global installs kept to a minimum
- CI and the workstation should provably run the same versions

## When not to use it

- The dependency is a **daemon** — Docker and containerd have to be on the host
- The team will not commit the config; an uncommitted environment reproduces nothing
- Disk is tight and nobody will garbage-collect `/nix/store`
- A container-based dev environment already covers it, and adding a second mechanism only confuses things

## Notes

**Nix underneath.** Devbox is a wrapper over the Nix package manager. Packages come from `nixpkgs`,
and <https://www.nixhub.io/> is the searchable index of which versions are available — the practical
answer to "can I pin `kubectl` to exactly this version?".

**Lifecycle:**

```sh
devbox init            # run once, creates the file structure
devbox shell           # enter the environment
exit                   # leave it
devbox update          # update the packages listed in devbox.json
devbox version update  # update Devbox itself
```

**Auto-entering the shell in VS Code only.** The recorded hook:

```sh
echo 'if [ "$TERM_PROGRAM" = "vscode" ]; then devbox shell --config /home/andrey/projects/pikakube; fi' >> ~/.bashrc
source ~/.bashrc
```

The `$TERM_PROGRAM` guard is the point: entering a Devbox shell on **every** terminal, including
non-project ones, is slow and confusing. Scoping it to the editor means the project environment is
active exactly where project work happens.

**Disk usage.** Packages live in `/nix/store`, which only ever grows:

```sh
sudo du -sh /nix/store
devbox run -- nix store gc --extra-experimental-features nix-command
```

The `--extra-experimental-features nix-command` flag is required because `nix store gc` is part of
the newer CLI, which Nix still gates behind an experimental flag. Without it the command simply
refuses to run, which reads as a broken command rather than a disabled feature.

**Migrating packages already installed by hand.** Before declaring anything, you need to know what
was installed manually and at which version:

```sh
apt-mark showmanual | sort     # what was installed deliberately, not as a dependency
apt list --installed | grep <name>   # which version
```

`apt-mark showmanual` is the right tool because it filters out the thousands of transitively
installed packages and leaves only the ones a human chose — the actual migration list.

**Recorded upstream issues, and what they force:**

- **JSON cannot hold comments** — <https://github.com/jetify-com/devbox/issues/2602>. The original
  note is direct about it: commenting a JSON list is awful, so a separate `devbox-comments.yaml`
  keeps the list of packages that *could* be used, with the reasoning attached. A workaround for a
  file-format decision, and worth knowing before wondering why two files exist.
- **Docker cannot run inside Devbox** —
  <https://github.com/jetify-com/devbox/issues/2485> and
  <https://github.com/NixOS/nixpkgs/issues/47201>. The daemon must be installed on the host. This is
  the hard boundary of the whole approach, not a gap to be closed later.
- **VS Code extensions need host binaries.** The recorded observation, phrased with visible
  irritation: Docker and `kubectl` have to be installed outside Devbox for the VS Code extensions to
  work, because adding an extension means installing its dependencies where the extension looks for
  them — the system `PATH`, not the project shell.

**After installing Docker on the host**, so it can be used without `sudo`:

```sh
sudo usermod -aG docker $USER
```

Group membership only takes effect on a new login session, which is why this appears not to work
until you log out and back in.

### The case for it, as originally written

The problem statement recorded alongside these notes is worth keeping intact, because it is the
justification rather than the mechanics:

- **Inconsistent environments** — replicating a setup across machines or teammates produces the
  classic "it works on my machine"
- **Complex dependency management** — several projects needing different versions of the same tool
- **Time-consuming setup** — hours of installing, configuring and checking compatibility
- **Global dependency conflicts** — one global version, many projects, guaranteed collisions
- **Lack of isolation** — a change made for one project silently affects another
- **Manual configuration** — hand-configured environments are inconsistent by construction
- **Collaboration difficulties** — different setups turn into integration problems
- **Environment drift** — setups diverge from the original over time, and the divergence is hard to trace
- **Slow onboarding** — new joiners spend their first day on setup, often following stale documentation
- **System pollution** — global installs clutter the host and cause version conflicts

And the outcome claimed for the solution: reproducible environments from a single `devbox.json`,
zero global installs, fast onboarding (clone and `devbox shell`), a disposable setup that leaves no
trace on the host, versioned and reproducible dependencies via Nix, shareable configuration for the
team, one file covering system packages and language runtimes alike, and developers spending time on
code rather than on setup.

---

[← Virtual environment](../README.md)
