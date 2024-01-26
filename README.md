## Overview

This is the source code for my personal website, [mosiman.ca](https://mosiman.ca). It's built with [zola](https://www.getzola.org/).

Previous iterations used Hugo, but I realized I had no idea how the themes worked. This time around, the theme is more or less done from scratch. Hopefully that means it's simple enough for me to understand a few months down the road.

## What's up with that build pipeline dawg

Yeah, I know. Why did you do that to yourself?

Basically, because in the templates we do something like

```
{{page.content | safe}}
```

Where `page.content` is html generated from processing the markdown file. We apply `safe` to it, and out comes proper html.

However, the tags (e.g. `h1`, `h2`, `p`, etc) are not styled. Ideally, we would wrap the entire contents with a css selector

```
<div class="markdown-content">
    {{ page.content | safe }}
</div>
```

And then we can override the styles for the tags inside that div.

```
.markdown-content p {
    # somehow apply tailwindcss's class="text-gray-600" to all <p> elements
}
```

So in the end, we need some css preprocessing. In particular, we use the `@apply` directive. We can use `tailwindcss` for now to generate the appopriate css. These styles are in `styles`, and the output gets dumped into `static/styles`.

Sorry future dillon.
