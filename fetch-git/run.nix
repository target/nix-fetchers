exec: fetch-git:
{ name ? "source", url, tag ? "", branch ? "", revision ? "" } @ args:
    # Effectively an enum:
    #
    # FetchGit:
    #  - Tag(tag)
    #  - Rev(branch, revision)

  let
    usageUnless = msg: cond: if cond then true else builtins.trace ''
fetch-git usage error:

    ${msg}

Fetch a tag:

   fetch-git { tag = "my-tag-name"; }

Fetch a revision:

  fetch-git { branch = "my-branch-name"; revision = "my-revision"; }

Received:

  fetch-git ${builtins.toJSON args}

Need help? Reach out at https://github.com/target/nix-fetchers.

'' false;

  in
  assert ((usageUnless "If the tag is specified, the branch and revision must be empty"
    ((tag != "") -> (branch == "" && revision == ""))));

  assert (usageUnless "If the branch is specified, revision must be, and tag must not be"
    ((branch != "") -> (revision != "" && tag == "")));

  assert (usageUnless "If the revision is specified, branch must be, and tag must not be"
    ((revision != "") -> (branch != "" && tag == "")));

if tag != "" then
  exec [
    "${fetch-git}/bin/fetch-git" name url "--tag" tag
  ]
 else
  exec [
    "${fetch-git}/bin/fetch-git" name url "--branch" branch revision
  ]
