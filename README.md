# Rule Parser

This is to help scrape data from web pages in more thorough and fleshed out ways. It will allow us to assign certain actions to happen everytime you see a specific pattern in the HTML's structure or data. It's an in-progress port of something I wrote at a previous internship to translate a webapp's interface to an iOS interface.

Essentially, this will map patterns (a string with special syntax) to a function that will be called every time that specific pattern is found.

These patterns will match anywhere on the page and will therefore be more resiliant against changes in the page's structure.

## Use Cases

### Wikipedia Data
Say we want to [gather data about which philosophers influence each other](http://www.coppelia.io/2012/06/graphing-the-history-of-philosophy/) using Wikipedia. We can write a few simple pattern rules to gather this data easily.

After looking at a philosopher's wikipedia page, we see this pattern:
```HTML
...
<tr>
	<td>
		<div class=NavHead> Influences </div>
		<ul class=NavContent>
			<li>
				<div>
					<div class=hlist>
						<ul>
							<li>
								<a href="/wiki/Christian_Wolff_(philosopher)" title="Christian Wolff (philosopher)">Wolff</a>
							</li>
							<li>
								<a href="/wiki/Christian_Wolff_(philosopher)" title="Christian Wolff (philosopher)">Wolff</a>
							</li>
							...
```
Clearly, this is gross and unweildly. However, we can automate some rules to be able to capture this data. Also, since the patterns are relative (they don't start from the very base of the HTML,) we can cut out anything that's unnessesary.

```
	(div : class=NavHead, text=Influences)
	 -- (ul : class=NavContent) =>* (li) => (a)

	look for a div with class NavHead that contains the text Influences
	then look for a ul tag that that div is on the same hierarchy with that has class NavContent
	look in all of the tags contained within the ul until you find an li tag which contains an a tag.

```
The syntax isn't implemented or designed yet, but this is just a possible query. However, we can then run some command to take the text of the final `a` tag that we found and put it into a graph.


## Viewing Examples

You can make an easy d3 visualization of the data. Go to `examples/` and start a server. If you have python, you can easily run 
```bash
python -m SimpleHTTPServer 8888
```
Then, navigate to `http://localhost:8888/`. 

You may need to open `index.html` to edit the `filename` variable to whatever `.json` file you have in your directory.