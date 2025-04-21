/*
	Create tango.py input file by webscraping

	Works as of 2025-04-20, but may break at any time
	No error checking (it's not worth it, since scraping is always ultrafragile)

	Usage:
	* Read and understand the code! Or at least ask an AI's opinion. Running unknown code in your browser is not a good idea.
	* Log in to linkedin
	* Navigate to https://www.linkedin.com/games/tango/
	* Open developer tools
	* Go to console tab
	* Paste this script and press enter
	* Copy console output to a text file
	* Run tango.py [input file]
*/


console.log((() => {
    const edgeArray = Array.from(Array(7).keys().map(() => '+')).join('-')
    const lineArray = Array.from(Array(7).keys().map(() => '|')).join(' ')
    const board = Array.from(Array(13).keys().map((i) => Array.from(i % 2 ? lineArray : edgeArray)))
    const mapEdges = {
        'Cross': 'x',
        'Equal': '=',
    }

    const cells = $x('//div[contains(@id, "lotka-cell-")]')
    cells.forEach(cell => {
        const id = cell.id.split('-')[2]
        const x = id % 6
        const y = Math.floor(id / 6)

        const content = document.evaluate('.//div[contains(@class, "lotka-cell-content--locked")]//*[name()="svg"]', cell, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null).iterateNext()
        if (content)
            board[y * 2 + 1][x * 2 + 1] = content.getAttribute('aria-label')[0]

        const edges = document.evaluate('.//div[contains(@class, "lotka-cell-edge")]', cell, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null)
        while (true) {
            const edge = edges.iterateNext()
            if (!edge)
                break

            const direction = edge.getAttribute('class').split('--')[1]
            const edgetype = document.evaluate('.//*[name()="svg"]', edge, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null).iterateNext().getAttribute('aria-label')

            if (direction === 'right')
                board[y * 2 + 1][x * 2 + 2] = mapEdges[edgetype]
            if (direction === 'down')
                board[y * 2 + 2][x * 2 + 1] = mapEdges[edgetype]
        }
    })
    return board.map((row) => row.join('')).join('\n')
})())
