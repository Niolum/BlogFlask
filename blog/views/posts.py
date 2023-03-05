from flask import Blueprint, render_template, request, flash, redirect, url_for

from blog import db


posts = Blueprint('posts', __name__, url_prefix='/posts')