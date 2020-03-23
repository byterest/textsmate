from flask import Blueprint, render_template, redirect, flash, url_for
from forms import WriteForm, EditForm
from models import Post
from exts import db
from translate import trans
from markupsafe import Markup
from flask_login import login_required, current_user
postbp = Blueprint('postbp', __name__)

@postbp.route('/<int:id>')
def getpost(id):
    post = Post.query.filter(Post.id==id).first()
    body = trans(post.body)
    post = {
        'title':post.title,
        'body':Markup(body),
        'time':post.create_time.strftime('%b %d, %Y')
    }
    return render_template('post.html', post=post)


@postbp.route('/new', methods=['GET', 'POST'])
@login_required
def newpost():
    form = WriteForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,user=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash('can not')
    return render_template('new.html', form=form)


@postbp.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.filter(Post.id==id).first()
    form = EditForm(title=post.title,body=post.body)
    if current_user != post.user:
        flash("You do not have this permission to edit article")
        return redirect('/post/'+str(id))
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect('/post/'+str(id))
    else:
        flash("There is an error")
    return render_template('edit.html', form=form, id=id)

@postbp.route('/<int:id>/delete')
@login_required
def delete(id):
    post = Post.query.filter(Post.id==id).first()
    if current_user != post.user:
        flash("You do not have this permission to edit article")
        return redirect('/post/'+str(id))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('manage'))
