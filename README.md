# Convert Windows Cursor into X Cursor for GNOME

Thank you very much to every open-source contributor who has made contributions to `sd2xc`, including CSDN user [~yuyu](https://blog.csdn.net/qq_41172785), as well as all others who cannot be traced due to broken links.

During my usage, I encountered some difficulties, so I decided to organize and integrate everything into a `docker` image.

This docker image is certainly not the best, as it involves downloading packages, which is quite lengthy. However, the process of building it can serve as a reference.

By following the steps in the Dockerfile, you can eventually set it up and access it through http://your.domain or https://your.domain. Things need to be modified have been marked in `nginx.conf`.

Moreover, to facilitate convenience, I have integrated all into docker as service, using `flask` and `JavaScript`(no webpack). Currently, everyone can access it online by clicking [here](https://www.sakebow.cn).

It has no CSS, which might make it look quite basic. But, on the flip side, it's also very clear.

The page contains only a place to upload files and a submit button, and only files set and packaged by `CursorXP` with the extension `CurXPTheme` can be submitted. If the submission is successful, after a moment, the message "成功转换$X$个鼠标样式" will appear. If $X>0$, it means the conversion was successful, and a download link will appear beside.

Of course, if you want to do it yourself, I also have a tutorial [here](http://hexo.sakebow.cn/2024/02/14/custom/linux-change-cursor/).

# Current Bugs

Due to the page being too simple, there are many imperfections:

- [ ] The name of the submission is the original file name, which does not guarantee that the uploaded file won't be overwritten if another person uses the same file name;
- [ ] There was a little glitch in setting the download file, where the extension is the same as the file name (for example, it should be laffey.tar.gz, but the result is laffey.laffey). However, even so, it can still be recognized as tar.gz, and double-clicking allows for extraction. The reason for this has not yet been discovered;
- [ ] The function for timed file deletion has not been tested yet, requiring periodic manual maintenance.
- [ ] ...
