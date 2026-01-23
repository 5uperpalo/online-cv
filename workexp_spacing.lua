-- Pandoc filter to add spacing for Work Experience list items and smaller font for Publications
local in_work_exp = false
local in_publications = false

function Header(elem)
  if elem.level == 2 then
    local header_text = pandoc.utils.stringify(elem.content)
    if header_text == "Work Experience" then
      in_work_exp = true
      in_publications = false
      -- Return the header plus LaTeX commands to set spacing only for level 1, reset for nested
      return {elem, pandoc.RawBlock('latex', '\\setlist[itemize,1]{itemsep=0.5em, parsep=0.5em}\\setlist[itemize,2]{itemsep=0pt, parsep=0pt}\\setlist[itemize,3]{itemsep=0pt, parsep=0pt}')}
    elseif header_text == "Publications" then
      in_work_exp = false
      in_publications = true
      -- Return the header
      return elem
    else
      if in_work_exp then
        -- We've left Work Experience, reset spacing
        in_work_exp = false
        return {elem, pandoc.RawBlock('latex', '\\setlist[itemize,1]{itemsep=0pt, parsep=0pt}\\setlist[itemize,2]{itemsep=0pt, parsep=0pt}\\setlist[itemize,3]{itemsep=0pt, parsep=0pt}')}
      elseif in_publications then
        -- We've left Publications
        in_publications = false
        return elem
      end
    end
  end
  return elem
end

-- Apply smaller font to Publications list and maintain Work Experience spacing
function BulletList(elem)
  if in_publications then
    -- Wrap the list in a small font group - use proper LaTeX grouping
    return {
      pandoc.RawBlock('latex', '\\begingroup\\footnotesize'),
      elem,
      pandoc.RawBlock('latex', '\\endgroup')
    }
  end
  -- For Work Experience, just return the list (spacing is handled by \setlist)
  return elem
end
