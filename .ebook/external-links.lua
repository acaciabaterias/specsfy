function Link(link)
  if link.target:match("^%.%./develop/") then
    link.target = "https://github.com/promovaweb/specsfy/blob/main/docs/"
      .. link.target:gsub("^%.%./", "")
  elseif link.target:match("^%.%./%.%./") then
    local repository_path = link.target:gsub("^%.%./%.%./", "")
    local route = "blob"
    if repository_path:match("/$") then
      route = "tree"
    end
    link.target = "https://github.com/promovaweb/specsfy/"
      .. route
      .. "/main/"
      .. repository_path
  end
  return link
end

local function normalize_brand_assets(text)
  return text:gsub("[%.%/]*brand/logo/", "brand/logo/")
end

function Image(image)
  image.src = normalize_brand_assets(image.src)
  return image
end

function RawBlock(block)
  if block.format == "html" then
    block.text = normalize_brand_assets(block.text)
    block.text = block.text:gsub("<source([^>]*)>", "<source%1 />")
    block.text = block.text:gsub("<img([^>]*)>", "<img%1 />")
  end
  return block
end

function RawInline(inline)
  if inline.format == "html" then
    inline.text = normalize_brand_assets(inline.text)
  end
  return inline
end

local function is_logo_picture(block)
  if block.t ~= "Plain" then
    return false
  end
  for _, inline in ipairs(block.content) do
    if inline.t == "RawInline"
      and inline.text:match("<picture")
    then
      return true
    end
  end
  return false
end

function Pandoc(document)
  local blocks = {}
  local index = 1
  while index <= #document.blocks do
    local opening = document.blocks[index]
    local content = document.blocks[index + 1]
    local closing = document.blocks[index + 2]
    if opening
      and opening.t == "RawBlock"
      and opening.text:match('<p align="center">')
      and content
      and is_logo_picture(content)
      and closing
      and closing.t == "RawBlock"
      and closing.text:match("</p>")
    then
      local image = pandoc.Image(
        {pandoc.Str("Logo do Specsfy")},
        "brand/logo/icon.png",
        "",
        pandoc.Attr("", {"ebook-logo"}, {{"width", "128"}})
      )
      table.insert(
        blocks,
        pandoc.Div(
          {pandoc.Para({image})},
          pandoc.Attr("", {"ebook-logo-block"})
        )
      )
      index = index + 3
    else
      table.insert(blocks, opening)
      index = index + 1
    end
  end
  local result = pandoc.Pandoc(blocks, document.meta)
  local anchors = {}
  for _, block in ipairs(result.blocks) do
    if block.t == "Header" and block.level == 1 then
      local source = block.identifier:match("^(.-%.md)__")
      if source then
        source = source:lower()
        anchors[source] = anchors[source] or block.identifier
        local basename = source:match("([^_]+%.md)$")
        if basename then
          anchors[basename] = anchors[basename] or block.identifier
        end
      end
    end
  end

  return result:walk({
    Link = function(link)
      local target = link.target
      local key = target:match("^#(.+%.md)$")
      if not key and target:match("%.md$") then
        key = target
          :gsub("^%.%./", "")
          :gsub("/", "__")
        if not anchors[key] then
          key = target:match("([^/]+%.md)$")
        end
      end
      if key then
        key = key:lower()
      end
      if key and anchors[key] then
        link.target = "#" .. anchors[key]
      end
      return link
    end
  })
end
