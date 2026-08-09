[← Certifications](../README.md)

# LFCS

<https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/>
<https://learn.kodekloud.com/user/courses/labs-linux-foundation-certified-system-administrator-lfcs>

---

## The problem it solves

Linux Foundation Certified System Administrator is the layer beneath Kubernetes. Users and groups,
file permissions and ACLs, systemd, storage and LVM, networking, package management, and finding
things with `find` under time pressure.

It matters here for an unglamorous reason: **most cluster problems are node problems.** A pod that
will not start because the disk is full, a kubelet that will not come up because a systemd unit is
misconfigured, a DNS failure that is really `/etc/resolv.conf` — none of those are Kubernetes
problems, and Kubernetes knowledge does not fix them.

## When to use it

- Before or alongside [CKA](../cka/README.md); it is the foundation the cluster sits on
- Self-managed clusters, where the nodes are yours to keep alive
- Any role where "the node is unhealthy" is your problem rather than a support ticket

## When not to use it

- As a Kubernetes credential — it is not one, and does not claim to be
- If node-level access is not part of the job and never will be

## Notes

Five mock exams with worked answers sit beside this file — `mock1.md` through `mock5.md` — plus
`repositories.md`, a curated list of resources.

**The mocks are the substance.** They are written as question-then-answer, and the answers routinely
give several equivalent commands rather than one. From the first question of `mock1.md`, finding
files with the owner-execute bit set:

```sh
find /opt/findme/ -type f -perm -u=x > /opt/foundthem.txt
find /opt/findme/ -type f -perm /u=x  | tee /opt/foundthem.txt
```

And deleting SETUID files, with five variations recorded:

```sh
find /opt/findme/ -type f -perm -4000 -exec rm -f {} +
find /opt/findme/ -type f -perm -4000 | xargs rm -f
find /opt/findme/ -type f -perm /u=s -exec rm {} \;
find /opt/findme/ -perm /4000 -exec rm -f {} \;
find /opt/findme/ -perm /4000 -exec rm -f {} +
```

Listing alternatives rather than one answer is deliberate and is the right way to study this
material — under time pressure you need whichever form you can type correctly, not the elegant one.
The distinction the variations turn on is worth stating once, since it is the most common `find`
mistake: **`-perm -mode` means "all of these bits set"; `-perm /mode` means "any of these bits set";
`-perm mode` means "exactly this mode"**. And `-exec ... +` batches arguments into few invocations
while `-exec ... \;` runs once per file — the difference between fast and very slow on ten thousand
files.

The mocks begin with `sudo -i`, which is the practical exam habit: become root once rather than
prefixing everything.

**`repositories.md` is annotated, and the annotations are the point.** The original notes rate the
sources rather than just listing them:

- **"excellent theoretical summaries"** —
  <https://github.com/mx-ulises/certification-prep-cka-ckad/blob/main/lfcs/> and
  <https://github.com/ahsfar/LFCS-guide>
- **"mediocre"** — a group including the Linux Foundation's own practice-questions PDF, a KodeKloud
  PDF, and several repositories (`simonesavi/lfcs`, `giulianopz/lfcs`,
  `BabuRajan002/...`, `mrkeyongenesis/LFCS-Study-Guide`, `zorski/lfcs-course-notes`,
  `vsingh55/Linux-for-LFCS`, `elliotholden/lfcs-practice-exam`)
- **question mocks** — <https://github.com/thehaohcm/DevOpsLabs/tree/master/Linux/LFCS/Practices/Mock%20Tests>
  and <https://github.com/willher/LFCS-Practice-Exam>
- **"others"** — a longer tail of repositories kept without judgement:
  `CFCIfe/LFCS-Practice-Questions-Solutions`, `oscar-franzen/lfcs`, `karakays/lfcs`,
  `herringfromblr/lfcs_practice_labs`, `mymborrini/lfcs-notes`, `teleivo/lfcstraining`,
  `craig91/LFCS-Notes`, `oguzhalit/lfcs-workshops`, `jjberrow/LFCS_Study_Guide`,
  `loyality7/lfcs-practice-tool`, `Haydenbuilds/lfcs-practice`,
  `chanchiwai-ray/lfcs-practice-questions`, `StenlyTU/LFCS-official`, `Ghada-Atef/LFCS-Lab-Scripts`,
  `gabrielemorini/lfcs`, `dvbrennanjv/PUB-LFCS-Notes`

A search returns all of these. Only someone who read them can say which two are the good ones, and
that judgement — including calling the official practice PDF mediocre — is the part of this file
worth preserving.

---

[← Certifications](../README.md)
