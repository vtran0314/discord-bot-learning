import uuid
import settings
from PIL import Image, ImageDraw, ImageFont

class RankImage:
    def draw_basic_information(
        self, display_name, total_points, current_rank, count_messages, count_reactions
        ):
        
        uuid4 = str(uuid.uuid4())
        
        img = Image.open(settings.IMAGES_DIR / "rank_bg.png")
        
        '''
        Ubuntu only have the following truetype in the system which is different from the video
        
        ls /usr/share/fonts/truetype/
        .uuid   dejavu/ ubuntu/
        maouque@DESKTOP-8BM3I4J:~/Discord-Bot-Fullstack$ ls /usr/share/fonts/truetype/ubuntu/
        .uuid              Ubuntu-BI.ttf      Ubuntu-L.ttf       Ubuntu-M.ttf       Ubuntu-R.ttf       Ubuntu-Th.ttf      UbuntuMono-BI.ttf  UbuntuMono-RI.ttf  
        Ubuntu-B.ttf       Ubuntu-C.ttf       Ubuntu-LI.ttf      Ubuntu-MI.ttf      Ubuntu-RI.ttf      UbuntuMono-B.ttf   UbuntuMono-R.ttf
        '''
        #font = ImageFont.truetype("/usr/share/fonts/truetype/", 28, encoding="unic")

        
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 20)
        
        draw = ImageDraw.Draw(img)
        
        draw.text(
            (180, 38),
            f"User: {display_name}",
            fill="black",
            font=font_big,
            anchor="ls")
        
        draw.text(
            (630, 38),
            f"Rank: {str(current_rank).rjust(4,'0')}",
            fill="black",
            font=font_big,
            anchor="rs"
            )
        
        draw.text(
            (180, 70),
            f"Total Points: {'%.2f' %total_points}",
            fill="black",
            font=font_small,
            anchor="ls"
            )
        
        draw.text(
            (180, 100),
            f"Total Messages: {count_messages}",
            fill="black",
            font=font_small,
            anchor="ls"
            )
        
        draw.text(
            (180, 130),
            f"Total Reactions: {count_reactions}",
            fill="black",
            font=font_small,
            anchor="ls"
            )
        
        full_image_path = settings.IMAGES_TMP_DIR / f"{uuid4}.png"

        img.save(full_image_path)
        return full_image_path
    

    def  draw_progress_bar(
        self, full_image_path, next_level_xp_diff, level_progress
        ):
        progress =  level_progress / next_level_xp_diff
        if progress == 1:
            progress = 0
            
        img = Image.open(full_image_path)
        
        draw = ImageDraw.Draw(img)
        
        full_width = 643
        width = full_width * progress
        
        #If x1 is < x0 it will raise error. For example x0 = 12 and x1 = 0
        # ValueError: x1 must be greater than or equal to x0
        #thus need to add 12.0 to meet requirement
        shape = ((12.0, 244.0), (width + 12.0, 290.0))
        draw.rectangle(xy=shape, fill="#0f0")
        
         
        font_small = ImageFont.truetype("UbuntuMono-B.ttf", 20)
        required_points = next_level_xp_diff - level_progress
        
        progress_percentage = round(progress * 100)
        
        draw.text(
            (full_width / 2, 270),
            f"{progress_percentage}% (Required Pts: {required_points})",
            fill = "black",
            anchor = "ms",
            font = font_small,
        )
        
        img.save(full_image_path)

    def draw_member_avatar(self, full_image_path, member_avatar_path):
        print (full_image_path)
        img = Image.open(full_image_path)
        avatar_img = Image.open(member_avatar_path)
        avatar_img.thumbnail((144, 144), Image.Resampling.LANCZOS)
        img.paste(avatar_img, (8,8))
        img.save(full_image_path)
        
        self.delete_img(member_avatar_path)
        
    def delete_img(self, full_image_path):
        full_image_path.unlink()