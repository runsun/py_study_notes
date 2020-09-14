# Push your repo to multiple repo sites

Ref: 

## For a new repo:

1. **bitbucket** Create a new repo "myrepo" in bitbucket

2. **github** Create a new "myrepo" in github

3. **local** go to local folder ".../" 

   ```
   ...>git clone git@bitbucket.org:runsun/myrepo.git
   ```

4. open file **config** 

   ```
   ...>cd myrepo/.git
   .../myrepo/.git/> (open the config in this folder)
   ```

5. **config**:  in the **[remote "origin"]** section, add line:

   ```
   url = git@github.com:runsun/py_study_notes.git 
   ```

That's it !!

## For an existing repo: (longer and more tedious)

==============================================

2020.5.14

We setup re_utils.py 

repo clone from github to be able to push to bitbucket as well.

Local:

** Change to folder ../re_utils.py > 

```
> git remote -v 
origin  https://github.com/runsun/re_utils.py.git (fetch)
origin  https://github.com/runsun/re_utils.py.git (push)
```

** Change from https to ssh (so we can use ssh to login directly)

```
> git remote set-url --delete origin https://github.com/runsun/re_utils.py.git
fatal: could not unset 'remote.origin.url'
> git remote rm origin
> git remove -v   # nothing!!
```

```
> git remote set-url --add origin git@github.com/runsun/re_utils.py.git
fatal: No such remote 'origin'
```

```
> git remote add origin git@github.com:runsun/re_utils.py.git
> git remote -v
origin  git@github.com:runsun/re_utils.py.git (fetch)
origin  git@github.com:runsun/re_utils.py.git (push)
```

** Copy the public key to the clipboard:

```
> clip < ~/.ssh/id_rsa.pub
```
```
> git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master

> git push --set-upstream origin master
Warning: Permanently added the RSA host key for IP address '140.82.114.4' to the list of known hosts.
Everything up-to-date
Branch master set up to track remote branch master from origin.
```
** Add bitbucket:

In bitbucket, I have the same repo but using different name: py_re_utilsIt contains older data so can be overwritten.

We also already have the ssh key setup, so skip that process for bitbucket. 

```
> git remote set-url --add origin git@bitbucket.org:runsun/py_re_utils.git
> git remote -v
origin  git@github.com:runsun/re_utils.py.git (fetch)
origin  git@github.com:runsun/re_utils.py.git (push)
origin  git@bitbucket.org:runsun/py_re_utils.git (push)
```
```
> git push
Everything up-to-date
To bitbucket.org:runsun/py_re_utils.git
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'git@bitbucket.org:runsun/py_re_utils.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. 
```

** Obviously it's hard to push to that repo. We create a new repo in bitbuck with the same name re_utils.py and add it to local remotes:

```
> git remote set-url --delete origin  git@bitbucket.org:runsun/py_re_utils.git
> git remote add origin git@bitbucket.org:runsun/re_utils.py.git
fatal: remote origin already exists.
```

```
> git remote set-url --add origin git@bitbucket.org:runsun/re_utils.py.git> git remote -v
origin  git@github.com:runsun/re_utils.py.git (fetch)
origin  git@github.com:runsun/re_utils.py.git (push)
origin  git@bitbucket.org:runsun/re_utils.py.git (push)
```
```
> git push
Warning: Permanently added the RSA host key for IP address '140.82.113.3' to the list of known hosts.
Everything up-to-date
Warning: Permanently added the RSA host key for IP address '18.205.93.2' to the list of known hosts.
Counting objects: 19, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (16/16), done.
Writing objects: 100% (19/19), 35.44 KiB | 930.00 KiB/s, done.
Total 19 (delta 6), reused 0 (delta 0)
To bitbucket.org:runsun/re_utils.py.git
 * [new branch]      master -> master
```


## References:

Must read: [How to properly mirror a git repository](http://blog.plataformatec.com.br/2013/05/how-to-properly-mirror-a-git-repository/)

amazon: [Push commits to an additional Git repository](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-mirror-repo-pushes.html)

stackoverflow: [Git push existing repo to a new and different remote repo server?](https://stackoverflow.com/questions/5181845/git-push-existing-repo-to-a-new-and-different-remote-repo-server)

jefferai . org: [Too Perfect a Mirror](http://web.archive.org/web/20130326115327/http://jefferai.org/2013/03/24/too-perfect-a-mirror/)