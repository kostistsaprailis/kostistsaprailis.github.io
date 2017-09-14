---
layout: post
title: "How to not make a blog, or how I stopped worrying and love breaking stuff."
date: 2016-05-09 19:33:42 +0300
excerpt: "These are my thoughts on trying to build a blog with the latest 'cool' thing called GithubPages + Jekyll."
categories: [blog]
comments: true
---

<!--excerpt-->

### Hello there!

These are my thoughts on trying to build a blog with the latest "cool" thing called GithubPages + Jekyll.

If you have never heard about it before, it's basically using "free" web hosting on
[GithubPages][githubpages-url] plus a static website generator engine called
[Jekyll][jekyll-url].

There are many great tutorials to get you started, one being an official
[Jekyll Guide][jekyllgithub-url] which gives an overview of how to integrate
the two and a second one, the more [analytical][jonathanmacglone-url] by
Jonathan McGlone.

However having Jekyll on its own does not really help with making a blog that
looks nice, especially if you're a developer like me who has no idea how to
design anything better than a napkin.

So what does anyone do when need something? Ask <del>our Supreme Overlord</del> Google
for a nice theme. The one I found that I really liked was [Hyde][hyde-url]. It's a
two column theme that was pretty much what I was looking for.

I just went ahead, and put everything together, trying to make it work. Usually
that's not the proper way to do something in a professional setting, however when
trying out a new project I think this is a better way to get a good understanding
of how different parts come together.

### How to do it wrong

To dive right in I downloaded Jekyll and created a new site. Then begun the hard part.
How do I integrate Hyde? Hyde is itself built upon a set of foundation setup called
[Poole][poole-url], however Hyde already contains all Poole code that is needed so
I decided to just head over to the [Hyde codebase][hydecode-url] and try to copy all
code tha seemed relevant. After a bit of back and forth and deleting what I thought
was not needed/I didn't want on my blog I thought I was ready to go.

The major problem I encountered was that the blog would stubbornly not show any blog posts.

Turns out I was missing the paginate gem (Jekyll engine is based on ruby) and also
two necessary config items.

After a lot of search, and feedback from Google I managed to get it working.

<strong>Note to self:</strong> Code on config files is usually necessay,
do not delete without checking the outcome.

The next challenge encountered was how to integrate a custom domain name. GithubPages
already provide the [username].github.io url for the page, where [username] is your
github one, however I always wanted a customer domain and now was the time to get it.

Everyone knows the basics of how domains work: you have a server that matches URLS to IPs
however how do you actually make assign one to the other?

A(ddress) and CNAME Records

[A-records][arecord-url] are basically mappings that return a 32-bit IPv4 address. They are used
by your domain registrar to let them know where you want the URL you just bought
though them to direct to.

In our case Github provides two IP addresses to map to. However how does Github know
which site (Github URL) to direct the request to?

Enter [CNAME][cname-url] records. As described by wikipedia:
> A Canonical Name record (abbreviated as CNAME record) is a type of resource record
in the Domain Name System (DNS) used to specify that a domain name is an alias for another domain,
the "canonical" domain. All information, including subdomains, IP addresses, etc.,
are defined by the canonical domain.

So what we are basically doing with this file is map the external URL (in my case
tsaprailis.com) to the internal URL that Github knows kostistsaprailis.github.io.


### Is the hassle worth it?

So enough with the rant, was it actually worth it?

That's not a straightfoward answer. There are currently far easier ways to start a blog
(Wordpress, Medium etc), why go through all the hassle to make it from scratch?

Well, what drew me to Jekyll is that as a developer I'm always
enjoying more building stuff myself. Having exposure to the underlying code is
always a great strength that allows you to configure (and also break) a project,
and also provide valuable knowledge.

So take something apart, break it and then try to make it work. You will always be
more motivated to make it work again. Go break stuff!


[githubpages-url]: https://pages.github.com/
[jekyll-url]: https://jekyllrb.com/
[jekyllgithub-url]: https://jekyllrb.com/docs/github-pages/
[jonathanmacglone-url]: http://jmcglone.com/guides/github-pages/
[hyde-url]: http://hyde.getpoole.com/
[poole-url]: http://getpoole.com/
[hydecode-url]: https://github.com/poole/hyde/
[arecord-url]:https://en.wikipedia.org/wiki/List_of_DNS_record_types#A
[cname-url]:https://en.wikipedia.org/wiki/CNAME_record
