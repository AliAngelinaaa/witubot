import discord
from discord.ext import commands

class ModerationCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Kick Command with Reason Argument
  @commands.command()
  @commands.has_permissions(kick_members=True)  # Restricts command to users with "Kick Members" permission
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
      await ctx.send("You cannot kick yourself!")
      return
    try:
      # Send DM based on member roles with improved error handling
      try:
        if "unverify" in [role.name for role in member.roles]:  # Replace with actual role name
          await member.send(f"""Dear {member.name},

We regret to inform you that your application to join the WITU community was not successful at this time.

Here are some reasons why your application may not have been accepted:

* **CUNY Affiliation:** Our community is primarily for individuals affiliated with the City University of New York (CUNY) as students, faculty, or alumni.
* **Gender**:  Currently, WITU is a women-focused community. We have exceptions for a limited number of individuals who have gone through a rigorous screening process. 
* **Community Guidelines:** Your application may not have been met our community guidelines.

We appreciate your interest in WITU, and we wish you the best of luck in your future endeavors.

Sincerely,
The WITU Team
""")
        else:
          await member.send(f"You have been kicked from WITU for violation of the rules")
      except discord.HTTPException as e:
        print(f"Failed to send DM to {member.name} ({e})")
        await ctx.send(f"Failed to send DM to {member.name}. Reason: {e}")
      await member.kick(reason=reason)
    except discord.Forbidden:
      await ctx.send(f"I don't have the permissions to kick {member.name}.")
    except discord.HTTPException as e:
      await ctx.send(f"Failed to kick {member.name}. Reason: {e}")
  

  # Verification
  @commands.command(name ="verify")
  async def verify(self, ctx, member: discord.Member, *, reason=None):
    """
    This function verifies a member by removing the "unverify" role and sends a welcome DM.

    Args:
        ctx (discord.ext.commands.Context): The command context.
        member (discord.Member): The member object to verify.
        reason (str, optional): Optional reason for verification. Defaults to None.
    """

    if member == ctx.author:
      await ctx.send("You cannot verify yourself!")
      return

    try:
      # Attempt to remove "unverify" role and get verified role
      unverified_role = discord.utils.get(ctx.guild.roles, name="unverify")
      await member.remove_roles(unverified_role, reason=reason)
      await member.send(f"""#  🎉Welcome to WITUnite!🎉 

Congratulations! You're now verified and officially part of our community. 🌟  

To enhance your experience, please select your roles from the available options and take a moment to introduce yourself to fellow members. Your voice matters, and we're excited to have you here!

If you have any questions or need assistance, don't hesitate to reach out to our friendly moderators. 

Once again, welcome aboard! We can't wait to see you thrive within the WITUnite community. 💪✨
""")
    except discord.Forbidden:
      await ctx.send(f"I don't have the permissions to verify {member.name}.")
    except discord.HTTPException as e:
      await ctx.send(f"Failed to verify {member.name} ({e})")


async def setup(bot): # Must have a setup function
  await bot.add_cog(ModerationCommands(bot))