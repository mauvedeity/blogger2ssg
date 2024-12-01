# blogger2ssg

Project to map a Blogger XML dump to something that you could put into a static site generator.

## Notes

We will optionally require [`pandoc`](https://pandoc.org/) to work, because it translates the body of the posts from HTML to Markdown.

## TODO

We're going to produce the HTML body as `postname.html`, then call `pandoc` (if present and requested) to create `postname.md`.
Then we will create `postname.yaml` to cover the front matter (if requested).
The HTML file will have its file system date set to the post date so that it will import OK. We don't need to with Markdown
files because that's what the YAML is for.

## Front Matter

We're going to allow front matter:

* title, author, tags, date (pubdate unless there's an an updated date which is later)

```yaml
---
  title: Clean Dry Surface
  author: Mauvedeity
  tags:
    - reviews
    - surfacereview
    - hardware
  date: 2024-05-20T18:33:00.001+01:00
---
```

The tags come from the XML:

```xml
<category scheme='http://www.blogger.com/atom/ns#' term='surfacereview' />
```

There are  list of these values - I think Eleventy uses them. Basically we'll stick this front matter into the `postname.yaml` file, and we can then combine if needed.


## Images

We're going to have to parse the extracted HTML, and do the following:

### Links

Change the links from external to internal and relative. We are recreating the folder path and slug so should be OK. We also need to remap the extension to md if we're targeting Markdown.

### Images

For these, we can extract the path from the ```<img>``` tag. We can then pull down the file (if it doesn't exist already) to a file. Then rewrite the image path in the link to be local and relative (perhaps ```/image/``` or some such.
)